import os
import requests
import csv
import pkg_resources
from datetime import datetime
from bs4 import BeautifulSoup
from netCDF4 import Dataset, date2num


DATADIR = pkg_resources.resource_filename(__name__, "")


request_url = "http://views.cira.colostate.edu/fed/Reports/RawDataReport2.aspx"
datasets = {
    "improve aerosol": {
        "id": 10001,
        "df": "Daily",
        "site_file": os.path.join(DATADIR, "fedsites_improve_aerosol.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_improve_aerosol.csv"),
    },
    # castnet ozone hourly
    "castnet": {
        "id": 23005,
        "df": "Hourly",
        "site_file": os.path.join(DATADIR, "fedsites_castnet.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_castnet.csv"),
    }
}


class InputError(Exception):
    pass


class NotImplementedError(Exception):
    pass


def validate_input(dataset, site, parameter):

    # dataset
    if dataset not in datasets.keys():
        print(
            'dataset {} is not implemented.\n'.format(dataset) +
            'implemented datasets are:'
        )
        for dataset in datasets.keys():
            print("'{}'".format(dataset))
        raise(InputError)

    # site
    site_info = get_site_info(dataset, site)
    if not site_info:
        print(
            'site-code {} is not available.\n'.format(site) +
            'available sites are:'
        )
        site_codes = get_all_site_codes(dataset)
        for site_code in site_codes:
            site_info = get_site_info(dataset, site_code)
            print("{}: {}".format(site_code, site_info))
        raise(InputError)

    # parameter
    parameter_info = get_parameter_info(dataset, parameter)
    if not parameter_info:
        print(
            'parameter-code {} is not available.\n'.format(parameter) +
            'available parameters are:'
        )
        with open(datasets[dataset]["parameter_file"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print(row)
        raise(InputError)

    return True


def set_request_data(
        dataset_id, site_id, parameter_id, df, start_date, end_date):
    return {
        "agidse": 1,
        "dt": "{0}>{1}".format(
            start_date.strftime("%Y/%m/%d"),
            end_date.strftime("%Y/%m/%d")
        ),
        "dsidse": dataset_id,
        "op": [
            "OutputFormat-AsciiText",
            "OutputMedium-File",
            "FilePartitioning-Single",
            "ColumnFormat-Delimited",
            "RowFormat-Pivot",
            "Delimiter-;",
            "ContentType-DataAndMetadata",
            "ColumnHeaders-true",
            "SectionTitles-true",
            "StringQuotes-None",
            "MissingValues--999",
            "DateFormat-101",
        ],
        "fi": [
            "Dataset.DatasetCode",
            "Site.SiteCode",
            "AirFact.POC",
            "AirFact.FactDate",
            "AirFact.FactValue",
            "AirFact.Unc",
            "AirFact.StatusFlag",
            "AirFact.Flag1",
            "AirFact.Flag2",
            "AirFact.Flag3",
            "AirFact.Flag4",
            "AirFact.Flag5",
        ],
        "siidse": site_id,
        "paidse": parameter_id,
        "df": df,
        "qscs": "load",
        "dttype": 1,
    }


def get_site_info(dataset, site_code):
    '''returns a dict with information of the site
       as contained in the site file
    '''
    site_info = {}
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                header = row
            else:
                if row[1] == site_code:
                    for item, value in zip(header, row):
                        site_info[item] = value
    return site_info


def get_all_site_codes(dataset):
    '''returns a list of containing all site codes
       (e.g. BADL1)
       within the site file of the dataset
    '''
    site_codes = []
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count > 0:
                site_codes.append(row[1])
    return site_codes


def get_parameter_info(dataset, parameter_code):
    '''returns a dict with information of the parameter
       as defined by the parameter file
    '''
    parameter_info = {}
    with open(datasets[dataset]["parameter_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                header = row
            else:
                if row[2] == parameter_code:
                    for item, value in zip(header, row):
                        parameter_info[item] = value
    return parameter_info


def get_data(request_data):
    '''returns a dict of parsed data retrived from the
       Federal Land Manager Environmental Database
       http://views.cira.colostate.edu/fed/QueryWizard/
    '''
    r = requests.post(request_url, data=request_data)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find("a")
    href = link.get('href')
    url_base = "http://views.cira.colostate.edu"
    url_txt = url_base + href
    r_txt = requests.get(url_txt)
    return parse_fed_data(r_txt.text)


def parse_fed_data(text):
    '''returns a dict of parsed data
    '''
    def get_row_nr(rows, string):
        start_row_nr = [
            row_nr for row_nr, row in enumerate(rows) if row == string
        ][0] + 2
        end_row_nr = start_row_nr + [
            index for index, row in enumerate(rows[start_row_nr::]) if row == ''
        ][0]
        return (start_row_nr, end_row_nr)

    def get_data_dict(rows):
        datarows = list(csv.reader(rows, delimiter=';'))
        datadict = {}
        for column_nr in range(len(datarows[0])):
            datadict[datarows[0][column_nr]] = [
                row[column_nr] for index, row in enumerate(datarows)
                if index > 0
            ]
        return datadict

    rows = text.replace("\r", '').split("\n")

    data = {}
    for item in ["Datasets", "Sites", "Parameters", "Status Flags", "Data"]:
        (start_row_nr, end_row_nr) = get_row_nr(rows, item)
        data[item.lower()] = get_data_dict(
            rows[start_row_nr : end_row_nr])

    try:
        data["data"]["Date"] = [
            datetime.strptime(date_i, '%m/%d/%Y %H:%M:%S')
            for date_i in data["data"]["Date"]
        ]
    except ValueError:
        data["data"]["Date"] = [
            datetime.strptime(date_i, '%m/%d/%Y')
            for date_i in data["data"]["Date"]
        ]

    return {
        "data_version": "",  # FIXME
        "station_name": data["sites"]["Site"][0],
        "station_code": data["sites"]["Code"][0],
        "station_category": "global",
        "observation_category": (
            "Air sampling observation at a stationary platform"
        ),
        "country_territory": "",  # empty should be ok
        "contributor": data["datasets"]["Dataset"][0].split(' ')[0].lower(),
        "latitude": data["sites"]["Latitude"][0],
        "longitude": data["sites"]["Longitude"][0],
        "altitude": data["sites"]["Elevation"][0],
        "nr_of_sampling_heights": "1",
        "sampling_heights": "",  # empty should be ok
        "contact_point": "nmhyslop@ucdavis.edu",
        "dataset": data["datasets"]["Dataset"][0],
        "parameter": data["parameters"]["Parameter"][0],
        "parameter_code": data["parameters"]["Code"][0],
        "time_interval": data["datasets"]["Frequency"][0].lower(),
        "measurement_unit": data["parameters"]["Units"][0].replace("Âµ", 'u'),
        "measurement_method": "",  # empty should be ok
        "sampling_type": "continuous",
        "time_zone": "UTC",
        "measurement_scale": "",  # empty should be ok
        "status_flags": data["status flags"],
        "data": data["data"]
    }


def get_output_filename(data, extension):
    '''returns a filename conating the follwoing parts

       [Station code].[Contributor].[Observation category].
       [Sampling type].[Parameter].[Auxiliary item].[Data type].

       ex: ryo239n00.jma.as.cn.cfc113.nl.hr2007.dat

       [Observation category]
         as: Air observation at a stationary platform
         am: Air observation by a mobile platform
         ap: Vertical profile observation of air
         tc: Total column observation at a stationary platform
         hy: Hydrographic observation by ships
         ic: Ice core observation
         sf: Observation of surface seawater and overlying air

       [Sampling type]
         cn: Continuous or quasi-continuous in situ measurement
         fl: Analysis of air samples in flasks
         fi: Filter measurement
         rs: Remote sensing
         ic: Analysis of ice core samples
         bo: Analysis of samples in bottles
         ot Other

       [Data type]
         ev: Event sampling data
         om: One-minute mean data
         tm: Ten-minute mean data
         hrxxxx: Hourly mean data observed in the year xxxx
         da: Daily mean data
         mo: Monthly mean data

       [Auxiliary item]
         If a data file is NOT identified uniquely with the codes above,
         this field is filled with some characters to give a unique
         filename.
         nl: Null
    '''
    if data["observation_category"] == (
            "Air sampling observation at a stationary platform"):
        observation_category = "as"
    else:
        raise(NotImplementedError)

    if data["sampling_type"] == "continuous":
        sampling_type = "cs"
    else:
        raise(NotImplementedError)

    if data["time_interval"] == "daily":
        data_type = "da"
    elif data["time_interval"] == "hourly":
        data_type = "hr{}".format(data["data"]["Date"][0].year)
    else:
        raise(NotImplementedError)

    return "{0}.{1}.{2}.{3}.{4}.{5}.{6}.{7}".format(
        data["station_code"].lower(),
        data["contributor"],
        observation_category,
        sampling_type,
        data["parameter_code"].lower(),
        "nl",
        data_type,
        extension
    )


def save_data_txt(out_dir, data):
    """
        the 'World Data Centre' format is used,
        It has 32 header lines which describes the site and data,
        then the data-records.
        # TODO: fix format (discussion with dave)
    """

    nr_digits_date = 10
    nr_digits_time = 5
    nr_digits_data = 10
    nr_digits_nd = 5
    nr_digits_sd = 7
    nr_digits_f = 5
    nr_digits_cs = 2
    nr_digits_rem = 9

    header_lines = 32

    title = "{0} {1} mean data".format(
        data["parameter_code"], data["time_interval"])

    file_name = get_output_filename(data, "dat")

    data_format = "Version 1.0"
    total_lines = header_lines + len(data["data"]["Date"])

    covering_period = "{0} {1}".format(
        data["data"]["Date"][0].strftime("%Y-%m-%d"),
        data["data"]["Date"][-1].strftime("%Y-%m-%d")
    )

    file_header_rows = [
        "C01 TITLE: {}".format(title),
        "C02 FILE NAME: {}".format(file_name),
        "C03 DATA FORMAT: {}".format(data_format),
        "C04 TOTAL LINES: {}".format(total_lines),
        "C05 HEADER LINES: {}".format(header_lines),
        "C06 DATA VERSION: {}".format(data["data_version"]),
        "C07 STATION NAME: {}".format(data["station_name"]),
        "C08 STATION CATEGORY: {}".format(data["station_category"]),
        "C09 OBSERVATION CATEGORY: {}".format(data["observation_category"]),
        "C10 COUNTRY/TERRITORY: {}".format(data["country_territory"]),
        "C11 CONTRIBUTOR: {}".format(data["contributor"]),
        "C12 LATITUDE: {}".format(data["latitude"]),
        "C13 LONGITUDE: {}".format(data["longitude"]),
        "C14 ALTITUDE: {}".format(data["altitude"]),
        "C15 NUMBER OF SAMPLING HEIGHTS: {}".format(
            data["nr_of_sampling_heights"]),
        "C16 SAMPLING HEIGHTS: {}".format(data["sampling_heights"]),
        "C17 CONTACT POINT: {}".format(data["contact_point"]),
        "C18 PARAMETER: {}".format(data["parameter_code"]),
        "C19 COVERING PERIOD: {}".format(covering_period),
        "C20 TIME INTERVAL: {}".format(data["time_interval"]),
        "C21 MEASUREMENT UNIT: {}".format(data["measurement_unit"]),
        "C22 MEASUREMENT METHOD: {}".format(data["measurement_method"]),
        "C23 SAMPLING TYPE: {}".format(data["sampling_type"]),
        "C24 TIME ZONE: {}".format(data["time_zone"]),
        "C25 MEASUREMENT SCALE: {}".format(data["measurement_scale"]),
        "C26 CREDIT FOR USE: This is a formal notification for data users. 'For scientific purposes, access to these data is unlimited",  # noqa
        "C27 and provided without charge. By their use you accept that an offer of co-authorship will be made through personal contact",  # noqa
        "C28 with the data providers or owners whenever substantial use is made of their data. In all cases, an acknowledgement",  # noqa
        "C29 must be made to the data providers or owners and the data centre when these data are used within a publication.'",  # noqa
        "C30 COMMENT:",
        "C31",
        "C32 {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(
            "DATE".rjust(nr_digits_date - 4),
            "TIME".rjust(nr_digits_time),
            "DATE".rjust(nr_digits_date),
            "TIME".rjust(nr_digits_time),
            "DATA".rjust(nr_digits_data),
            "ND".rjust(nr_digits_nd),
            "SD".rjust(nr_digits_sd),
            "F".rjust(nr_digits_f),
            "CS".rjust(nr_digits_cs),
            "REM".rjust(nr_digits_rem)
        )
    ]

    with open(os.path.join(out_dir, file_name), mode='wb') as outfile:
        for row in file_header_rows:
            print(row)
            outfile.write("{}\n".format(row).encode("ascii"))

        for index in range(len(data["data"]["Date"])):
            if index > 0:

                value = data["data"][":Value"][index]
                value = value if not value == '-999' else "-99999.999"

                unc = data["data"][":Unc"][index]
                unc = unc if not unc == '-999' else "-999.99"

                outfile.write(
                    "{0} 9999-99-99 99:99 {1} {2} {3} {4} {5} {6}\n".format(
                        data["data"]["Date"][index].strftime("%Y-%m-%d %H:%M"),
                        "{:10.3f}".format(float(value)),
                        "-9999",
                        "{:7.2f}".format(float(unc)),
                        str(data["status_flags"]["Status Flag"].index(
                            data["data"][":StatusFlag"][index])).rjust(
                                nr_digits_f),
                        "-9",
                        "-99999999",
                    ).encode("ascii")
                )


def save_data_netcdf(out_dir, data):

    # TODO: fix format (talk to dave)

    file_name = get_output_filename(data, "nc")

    output_file = os.path.join(out_dir, file_name)
    dataset = Dataset(output_file, "w", format="NETCDF4")

    # global attributes

    dataset.station_name = data["station_name"]
    dataset.latitude = float(data["latitude"])
    dataset.longitude = float(data["longitude"])
    dataset.altitude = float(data["altitude"])

    # dimensions

    n = len(data["data"]["Date"])
    timedim = dataset.createDimension("time", n)
    chardim = dataset.createDimension('nchar', 2)

    # time

    time = dataset.createVariable("time", "f8", (timedim.name,))
    time.standard_name = "time"
    time.long_name = "time of measurement"
    time.units = "days since 1900-01-01 00:00:00 UTC"
    time.calendar = "gregorian"
    time[:] = [
        date2num(date_i, time.units, calendar=time.calendar)
        for date_i in data["data"]["Date"]
    ]

    parameter = dataset.createVariable(
        data["parameter_code"], "f8", (timedim.name,), fill_value=-9999.)
    parameter.standard_name = data["parameter"]
    parameter.missing_value = -9999.
    parameter.units = data["measurement_unit"]
    parameter[:] = data["data"][":Value"]

    # uncertainty

    parameter = dataset.createVariable(
        "Unc", "f8", (timedim.name,), fill_value=-9999.)
    parameter.standard_name = "Uncertainty"
    parameter.missing_value = -9999.
    parameter.units = data["measurement_unit"]
    parameter[:] = data["data"][":Unc"]

    # status flag

    parameter = dataset.createVariable(
        "SF", "c", (timedim.name, chardim.name))
    parameter.standard_name = "StatusFlag"
    description = ""
    for index in range(len(data["status_flags"]['Status Flag'])):
        description += "{0}: {1};".format(
            data["status_flags"]["Status Flag"][index],
            data["status_flags"]["Description"][index],
        )
    parameter[:] = data["data"][":StatusFlag"]

    dataset.close()
