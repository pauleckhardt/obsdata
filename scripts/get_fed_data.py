#!/usr/bin/env python3
import argparse
from datetime import datetime
from obsdata import (
    fed_config,
    fed_data,
    save_data
)


def get_and_save_data(
        dataset, site, parameter, start_date, end_date, data_format, out_dir):

    site_info = fed_config.get_site_info(dataset, site)

    parameter_info = fed_config.get_parameter_info(dataset, parameter)

    request_data = fed_data.set_request_data(
        fed_config.datasets[dataset]["id"],
        site_info["SiteID"],
        parameter_info["ParameterID"],
        fed_config.datasets[dataset]["df"],
        start_date,
        end_date
    )

    data = fed_data.get_data(request_data)
    data = data._replace(country_territory=site_info["CT"])
    if data_format == "nc":
        save_data.save_data_netcdf(out_dir, data)
    elif data_format == "dat":
        save_data.save_data_txt(out_dir, data)


def cli():

    # example showing how to retrieve data from the
    # Federal Land Manager Environmental Database
    # http://views.cira.colostate.edu/fed/QueryWizard/
    # and store the data in the 'World Data Centre' format

    # ./get_fed_data.py "improve aerosol" BADL1 OCf 2017-01-01 2017-01-31 -e dat -q /tmp  # noqa
    # ./get_fed_data.py "castnet" ABT147 O3 2014-01-01 2014-01-31 -e nc -q /tmp  # noqa

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset",
        metavar="dataset",
        type=str,
        help="fed dataset, e.g 'improve aerosol'"
    )
    parser.add_argument(
        "site_code",
        metavar="site-code",
        type=str,
        help="fed site code, e.g BADL1"
    )
    parser.add_argument(
        "parameter_code",
        metavar="parameter-code",
        type=str,
        help="parameter code e.g. OCf",
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
        default='nc',
        help='data format for saving file (nc or dat), default is nc (netcdf)',
    )
    parser.add_argument(
        '-q',
        '--datadir-for-save',
        dest='out_dir',
        type=str,
        default='/tmp',
        help='data directory for saving output, default is /tmp',
    )

    args = parser.parse_args()

    fed_config.validate_input(
        args.dataset,
        args.site_code,
        args.parameter_code
    )

    start_date = datetime.strptime(
        args.start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(
        args.end_date, '%Y-%m-%d').date()

    get_and_save_data(
        args.dataset,
        args.site_code,
        args.parameter_code,
        start_date,
        end_date,
        args.data_format,
        args.out_dir
    )


if __name__ == "__main__":

    cli()
