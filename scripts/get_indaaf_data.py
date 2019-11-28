#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from obsdata import (
    indaaf_config,
    indaaf_data,
    save_data
)


def get_indaaf_data(
        dataset_id, dataset_info, site_info, parameter_info,
        data_format, out_dir, csv_dir):

    parameter = parameter_info[
        "Parameter name"].values[0].replace(' ', '')

    out_filename = os.path.join(
        csv_dir,
        "{}-{}-{}.csv".format(
            dataset_info["name"], int(site_info.ID), parameter
        )
    )

    if indaaf_data.get_csv_file(
            dataset_id,
            int(site_info.ID),
            int(parameter_info.ID),
            out_filename):

        data = indaaf_data.get_records(
            out_filename,
            parameter,
            site_info,
            parameter_info,
            dataset_info
        )
        if dataset_info["time_interval"] == "hourly":
            year_start = data.records[0].start_datetime.year
            year_end = data.records[-1].start_datetime.year + 1
            for year in range(year_start, year_end):
                date_start = datetime(year, 1, 1)
                date_end = datetime(year + 1, 1, 1)
                filtered_records = save_data.date_filter_records(
                    date_start, date_end, data.records)
                if len(filtered_records) == 0:
                    continue
                current_data = data._replace(records=filtered_records)
                if data_format == "nc":
                    save_data.save_data_netcdf(out_dir, current_data)
                elif data_format == "dat":
                    save_data.save_data_txt(out_dir, current_data)
        else:
            if data_format == "nc":
                save_data.save_data_netcdf(out_dir, data)
            elif data_format == "dat":
                save_data.save_data_txt(out_dir, data)


def cli():

    # example showing how to retrieve data from
    # International Network to study Deposition and Atmospheric
    # chemistry in AFrica (INDAAF)
    # https://indaaf.obs-mip.fr/
    # and store the data in the 'World Data Centre' format

    # ./get_indaaf_data.py Gas 1 O3 -e dat -q /tmp  -x /tmp

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset_id",
        metavar="dataset_id",
        type=str,
        help="dataset_id. e.g 'Precipitation'"
    )
    parser.add_argument(
        "site_code",
        metavar="site-code",
        type=str,
        help="indaaf site code, e.g. 1 for 'Agoufou'"
    )
    parser.add_argument(
        "parameter_code",
        metavar="parameter-code",
        type=str,
        help="parameter code e.g. H+"
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
        '--datadir-for-csv',
        dest='csv_dir',
        type=str,
        default='/tmp',
        help='data directory for saving indaaf csv files, default is /tmp',
    )

    args = parser.parse_args()

    dataset_id = indaaf_config.get_dataset_id(
        args.dataset_id, int(args.site_code))
    if dataset_id == 0:
        print("Dataset not available.")

    dataset_info = indaaf_config.datasets[
        [row["name"] for row in indaaf_config.datasets].index(
            args.dataset_id)
    ]

    site_info = indaaf_config.validate_site_id(
        int(args.site_code))

    parameter_info = indaaf_config.get_parameter_id(
        args.parameter_code, args.dataset_id)

    get_indaaf_data(
        dataset_id,
        dataset_info,
        site_info,
        parameter_info,
        args.data_format,
        args.out_dir,
        args.csv_dir
    )


if __name__ == "__main__":
    cli()
