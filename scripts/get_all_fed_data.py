#!/usr/bin/env python3
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
        dataset,
        site_info.id,
        parameter_info.id,
        fed_config.datasets[dataset]["time_interval"],
        start_date,
        end_date
    )

    data = fed_data.get_data(request_data)
    if len(data.records) == 0:
        return
    data = data._replace(country_territory=site_info.country)
    if data_format == "nc":
        save_data.save_data_netcdf(out_dir, data)
    elif data_format == "dat":
        save_data.save_data_txt(out_dir, data)


if __name__ == "__main__":

    if 1:
        dataset = "10001"
        parameter = "OCf"
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2015, 12, 31)
        timedelta_month = 12 * 6
        data_format = "dat"
        out_dir = "/tmp"
    else:
        dataset = "23005"
        parameter = "O3"
        start_date = datetime(2011, 1, 1)
        end_date = datetime(2015, 12, 31)
        timedelta_month = 12
        data_format = "dat"
        out_dir = "/tmp"

    site_codes = fed_config.get_all_site_codes(dataset)
    for site_code in site_codes:
        date_i = start_date
        while date_i < end_date:
            date_j = (
                date_i +
                relativedelta(months=timedelta_month) -
                relativedelta(days=1)
            )
            print(site_code, date_i, date_j)
            get_and_save_data(
                 dataset,
                 site_code,
                 parameter,
                 date_i,
                 date_j,
                 data_format,
                 out_dir
            )
            date_i += relativedelta(months=timedelta_month)
        exit(0)
