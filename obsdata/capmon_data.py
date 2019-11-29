import os
import pandas as pd
from datetime import datetime
import requests
import numpy as np
from obsdata.save_data import ObsData, Record
from obsdata.capmon_config import datasets


def get_table_row_start(table_name, rows):
    for index, row in enumerate(rows):
        if row.startswith(b"*TABLE NAME //"):
            table_name_x = row.split(
                b",")[1].split(
                    b"//")[0].split(
                        b"\r")[0].decode("utf-8").strip()
            if table_name == table_name_x:
                return index
    return -1


def get_table_rows_data(rows, row_start):
    start = end = -1
    for index in range(row_start, len(rows)):
        if rows[index].startswith(b"*TABLE DATA BEGINS"):
            start = index
        if rows[index].startswith(b"*TABLE DATA ENDS"):
            end = index
            break
    return (start, end)


def get_data_from_row(rows, row_start, row_end, row_id):
    for index in range(row_start, row_end):
        if row_id in rows[index].split(b",")[0]:
            column_names = rows[index].split(b",")[1:]
            return [
                header.split(
                    b"//")[0].decode(
                        "utf-8").split(
                            "\r")[0].replace(
                                '"', "").strip() for header in column_names]
    return -1


def get_table_data(rows, row_start, row_end, headers):
    data = {}
    for header in headers:
        data[header] = []
    for row in rows[row_start + 1: row_end]:
        for index, header in enumerate(headers):
            try:
                data[header].append(
                    row.split(
                        b',')[1:][index].split(
                            b"//")[0].replace(
                                b"\xc9", b"E").decode(
                                    "utf-8").strip().replace('"', ""))
            except IndexError:
                data[header].append(np.nan)
    return pd.DataFrame(data, columns=data.keys())


def get_data_from_csvfile(csv_file, table_name):
    with open(csv_file, "rb") as the_file:
        rows = the_file.readlines()
        row_start_table = get_table_row_start(table_name, rows)
        start, end = get_table_rows_data(rows, row_start_table)
        headers = get_data_from_row(
            rows, row_start_table, end, b"TABLE COLUMN NAME--SHORT FORM")
        return get_table_data(rows, start, end, headers)


def get_header(csv_file, table_name, parameter):
    with open(csv_file, "rb") as the_file:
        rows = the_file.readlines()
        row_start_table = get_table_row_start(table_name, rows)
        start, end = get_table_rows_data(rows, row_start_table)
        headers = get_data_from_row(
            rows, row_start_table, end, b"TABLE COLUMN NAME--SHORT FORM")
        chemical_formula = get_data_from_row(
            rows, row_start_table, end, b"TABLE COLUMN NAME--CHEMICAL FORMULA")
        return headers[chemical_formula.index(parameter)]


def get_units(csv_file, table_name, parameter):
    with open(csv_file, "rb") as the_file:
        rows = the_file.readlines()
        row_start_table = get_table_row_start(table_name, rows)
        start, end = get_table_rows_data(rows, row_start_table)
        units = get_data_from_row(
            rows, row_start_table, end, b"TABLE COLUMN UNITS")
        chemical_formula = get_data_from_row(
            rows, row_start_table, end, b"TABLE COLUMN NAME--CHEMICAL FORMULA")
        return units[chemical_formula.index(parameter)]


def status_flag_to_number(status_flag):
    return [
        "V0",  # 'Valid value'
        "V1",  # 'Valid value - below detection limit'
        "V2",  # noqa 'Valid value - extreme or unusual value assessed and considered valid'
        "V7",  # noqa 'Valid value - below detection limit and reported as the detection limit or lowest measureable value'
        "M1",  # 'Missing value - no value available'
        "M2",  # 'Missing value - invalidated by Principal Investigator'
    ].index(status_flag)


def get_datetime(date, time):
    return datetime.strptime(
        "{} {}".format(date, time), "%Y-%m-%d %H:%M:%S"
    )


def get_records(
        data,
        site_info,
        target_parameter,
        status_parameter,
        units, dataset,
        parameter,
        time_interval):
    records = []
    for _, row in data.iterrows():
        start_datetime = get_datetime(
            row["DateStartUTC"], row["TimeStartUTC"]
        )
        end_datetime = get_datetime(
            row["DateEndUTC"], row["TimeEndUTC"]
        )
        records.append(
            Record(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                value=float(row[target_parameter]),
                uncertainty=-999,
                status=status_flag_to_number(
                    row[status_parameter]),
                status_flag=row[status_parameter],
                nr_of_samples=-999,
            )
        )
    try:
        sampling_heights = site_info["SamplingHeightAG"].values[0]
    except KeyError:
        sampling_heights = "?"

    return ObsData(
        data_version="?",
        station_name=site_info["SiteName"].values[0],
        station_code=str(site_info["SiteID"].values[0]),
        station_category="global",
        observation_category=(
            "Air sampling observation at a stationary platform"),
        country_territory=site_info["CountryCode"].values[0],
        contributor="capmon",
        latitude=site_info["Latitude_deg"].values[0],
        longitude=site_info["Longitude_deg"].values[0],
        altitude=site_info["GroundElevAMSL_m"].values[0],
        nr_of_sampling_heights=1,
        sampling_heights=sampling_heights,
        contact_point="enviroinfo@canada.ca",
        dataset=dataset,
        parameter=parameter,
        parameter_code=parameter,
        time_interval=time_interval,
        measurement_unit=units,
        measurement_method="?",
        sampling_type="continuous",
        time_zone="UTC",
        measurement_scale="?",
        status_flags="?",
        records=records,
    )


def download_csvfile(dataset, year, outdir):
    """downloads a csv file and store it locally if not already exists
    """
    index = [ds["name"] for ds in datasets].index(dataset)

    url_download_csv = os.path.join(
        datasets[index]["baseurl"],
        datasets[index]["file_pattern"].format(year=year)
    )

    csv_file = os.path.join(
        outdir,
        datasets[index]["file_pattern"].format(year=year)
    )

    if os.path.isfile(csv_file):
        return True
    r = requests.get(url_download_csv)
    if not r.status_code == 200:
        print("{} not available".format(url_download_csv))
        return False

    with open(csv_file, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)
    return True


def merge_data_many_years(
        dataset, parameter, site_info, year_start, year_end, outdir):
    """merge data from many years for a given site and returns
       an instance of obsdata"""
    index = [ds["name"] for ds in datasets].index(dataset)
    counter = 0
    for year in range(year_start, year_end + 1):
        csv_file = os.path.join(
            outdir,
            datasets[index]["file_pattern"].format(year=year)
        )
        if not os.path.isfile(csv_file):
            continue
        data_i = get_data_from_csvfile(csv_file, dataset)
        data_site = data_i.loc[data_i.SiteID == site_info["SiteID"].values[0]]
        if counter == 0:
            data = data_site
            units = get_units(csv_file, dataset, parameter)
            header_of_parameter = get_header(
                csv_file, dataset, parameter
            )
        else:
            data = data.append(data_site, ignore_index=True)
        counter += 1
    if counter == 0:
        return -1
    return get_records(
        data,
        site_info,
        header_of_parameter,
        "{}_Flag".format(header_of_parameter),
        units,
        dataset,
        parameter,
        datasets[index]["time_interval"]
    )


def create_sites_file(dataset, year_start,  year_end, datadir):
    """creates a csv site file that contains a row for each
       site, this function assumes that product files are
       already downloaded"""
    index = [ds["name"] for ds in datasets].index(dataset)
    counter = 0
    for year in range(year_start, year_end + 1):
        csv_file = os.path.join(
            datadir,
            datasets[index]["file_pattern"].format(year=year)
        )
        if not os.path.isfile(csv_file):
            continue
        data_i = get_data_from_csvfile(csv_file, "Site information")
        if counter == 0:
            data = data_i
        else:
            data = pd.concat(
                [data, data_i]).drop_duplicates('SiteID').reset_index(drop=True)
        counter += 1
    data = data.dropna(axis='columns')
    data.to_csv(
        os.path.join(datadir, '{}_sites.csv'.format(dataset.lower())),
        index=False,
        header=True
    )
