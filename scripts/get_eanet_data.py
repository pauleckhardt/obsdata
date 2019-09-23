#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
import numpy as np
from obsdata import (
    eanet_config,
    eanet_data,
    save_data
)


def get_eanet_data(
        dataset, site, parameter, start_date, end_date,
        data_format, out_dir, xls_dir):

    xlsfiles = eanet_data.get_xlsfiles(
        xls_dir, dataset, start_date.year, end_date.year)

    # for these sites we have needed meta data
    list_of_eanet_sites = np.array([s.site for s in eanet_config.eanet_sites])

    list_of_sheets = [
        pd.read_excel(xlsfile, sheet_name=parameter)
        for xlsfile in xlsfiles
    ]

    # sheets = pd.read_excel(xlsfile, sheet_name=None).keys()
    list_of_sites_all_sheets = eanet_data.get_all_sites(list_of_sheets)

    if site == 'all':
        list_of_sites = list_of_sites_all_sheets
    else:
        list_of_sites = [site]

    for site in list_of_sites:

        if not np.any(list_of_eanet_sites == site):
            # if we not have meta data for this site
            continue

        eanet_site = eanet_config.eanet_sites[
            np.nonzero(list_of_eanet_sites == site)[0][0]]

        data = eanet_data.merge_data(
            list_of_sheets, eanet_site, dataset, parameter)

        if data_format == "nc":
            save_data.save_data_netcdf(out_dir, data)
        elif data_format == "dat":
            save_data.save_data_txt(out_dir, data)


def cli():

    # example showing how to retrieve data from
    # The Acid Deposition Monitoring Network inEast Asia (EANET)
    # https://monitoring.eanet.asia/document/public
    # and store the data in the 'World Data Centre' format

    # ./get_eanet_data.py 1 all SO2 2001-01-01 2017-12-31 -e dat -q /tmp  -x /tmp # noqa

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset_id",
        metavar="dataset_id",
        type=str,
        help="dataset_id: 1 for 'Dry Monthly'"
    )
    parser.add_argument(
        "site_code",
        metavar="site-code",
        type=str,
        help=(
            "eanet site code, e.g JPA001 for 'Rishiri'," +
            " use 'all' for getting data from all available sites"
        )
    )
    parser.add_argument(
        "parameter_code",
        metavar="parameter-code",
        type=str,
        help=(
            "parameter code e.g. SO2, " +
            " use 'all' for getting data from all available parameters"
        )
    )
    parser.add_argument(
        "start_date",
        metavar="start-date",
        type=str,
        help="start date, format YYYY-MM-DD",
    )
    parser.add_argument(
        "end_date",
        metavar="end-date",
        type=str,
        help="end date, format YYYY-MM-DD",
    )
    parser.add_argument(
        '-e',
        '--data-format',
        dest='data_format',
        type=str,
        default='dat',
        help='data format for saving file (nc or dat), default is dat',
    )
    parser.add_argument(
        '-q',
        '--datadir-for-save',
        dest='out_dir',
        type=str,
        default='/tmp',
        help='data directory for saving output, default is /tmp',
    )
    parser.add_argument(
        '-x',
        '--datadir-for-xls',
        dest='xls_dir',
        type=str,
        default='/tmp',
        help='data directory for saving eanet xls files, default is /tmp',
    )

    args = parser.parse_args()

    start_date = datetime.strptime(
        args.start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(
        args.end_date, '%Y-%m-%d').date()

    if start_date < datetime(2001, 1, 1).date():
        print('start_date must be greater or equal to {}'.format(
            datetime(2001, 1, 1).date()))
        exit(1)
    if end_date > datetime(2017, 12, 31).date():
        print('end_date must be smaller or equal to {}'.format(
            datetime(2017, 12, 31).date()))
        exit(1)

    eanet_config.validate_input(
        args.dataset_id,
        args.site_code,
        args.parameter_code
    )
    if args.dataset_id == "1":
        dataset = "Dry Monthly"

    if args.parameter_code == 'all':
        parameters = eanet_config.Datasets[0]["parameters"]
    else:
        parameters = [args.parameter_code]

    for parameter in parameters:
        get_eanet_data(
            dataset,
            args.site_code,
            parameter,
            start_date,
            end_date,
            args.data_format,
            args.out_dir,
            args.xls_dir
        )


if __name__ == "__main__":
    cli()
