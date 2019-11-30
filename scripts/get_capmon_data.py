#!/usr/bin/env python3
import argparse
from datetime import datetime
from obsdata import (
    capmon_config,
    capmon_data,
    save_data
)


def get_capmon_data(
        dataset, parameter, site_info, date_start,
        date_end, data_format, out_dir, csv_dir):

    for year in range(date_start.year, date_end.year + 1):
        capmon_data.download_csvfile(dataset, year, csv_dir)

    data = capmon_data.merge_data_many_years(
        dataset, parameter, site_info,
        date_start.year, date_end.year, csv_dir)
    if data == -1:
        print("no data available.")
        exit(0)

    if data.time_interval == "hourly":
        for year in range(date_start.year, date_end.year + 1):
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
        filtered_records = save_data.date_filter_records(
                date_start, date_end, data.records)
        if len(filtered_records) == 0:
            return
        data = data._replace(records=filtered_records)
        if data_format == "nc":
            save_data.save_data_netcdf(out_dir, data)
        elif data_format == "dat":
            save_data.save_data_txt(out_dir, data)


def cli():
    # example showing how to retrieve data from Capmon
    # and store the data in the 'World Data Centre' format

    # noqa ./get_capmon_data.py CAPMoN_Precip_Chemistry CAPMCANS1KEJ "Cl-" 1986-01-01 1995-12-31 -e dat -q /tmp  -x /tmp
    # noqa ./get_capmon_data.py CAPMoN_Ozone CAPMCANS1KEJ O3 1986-01-01 1995-12-31 -e dat -q /tmp  -x /tmp

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset_id",
        metavar="dataset_id",
        type=str,
        help="dataset_id. e.g 'CAPMoN_Ozone'"
    )
    parser.add_argument(
        "site_code",
        metavar="site-code",
        type=str,
        help=(
            "capmon site code, e.g. CAPMCANS1KEJ "
            "for 'Kejimkujik National Park'"
        )
    )
    parser.add_argument(
        "parameter_code",
        metavar="parameter-code",
        type=str,
        help="parameter code e.g. O3"
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
        '--datadir-for-csv',
        dest='csv_dir',
        type=str,
        default='/tmp',
        help='data directory for saving indaaf csv files, default is /tmp',
    )

    args = parser.parse_args()

    start_date = datetime.strptime(
        args.start_date, '%Y-%m-%d')

    end_date = datetime.strptime(
        args.end_date, '%Y-%m-%d')

    capmon_config.validate_dataset(args.dataset_id)
    capmon_config.validate_parameter(
        args.dataset_id, args.parameter_code)
    site_info = capmon_config.get_site_info(
        args.dataset_id, args.site_code)

    get_capmon_data(
        args.dataset_id,
        args.parameter_code,
        site_info,
        start_date,
        end_date,
        args.data_format,
        args.out_dir,
        args.csv_dir
    )


if __name__ == "__main__":
    cli()
