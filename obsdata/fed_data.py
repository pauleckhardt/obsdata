import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from collections import namedtuple


FedData = namedtuple(
    "FedData",
    [
        "data_version",
        "station_name",
        "station_code",
        "station_category",
        "observation_category",
        "country_territory",
        "contributor",
        "latitude",
        "longitude",
        "altitude",
        "nr_of_sampling_heights",
        "sampling_heights",
        "contact_point",
        "dataset",
        "parameter",
        "parameter_code",
        "time_interval",
        "measurement_unit",
        "measurement_method",
        "sampling_type",
        "time_zone",
        "measurement_scale",
        "status_flags",
        "data",
    ]
)


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


def get_data(request_data):
    '''returns an instance of FedData where data are
       retrived from the
       Federal Land Manager Environmental Database
       http://views.cira.colostate.edu/fed/QueryWizard/
    '''
    request_url = "http://views.cira.colostate.edu/fed/Reports/RawDataReport2.aspx"  # noqa
    r = requests.post(request_url, data=request_data)
    soup = BeautifulSoup(r.content, 'html.parser')
    link = soup.find("a")
    href = link.get('href')
    url_base = "http://views.cira.colostate.edu"
    url_txt = url_base + href
    r_txt = requests.get(url_txt)
    return parse_fed_data(r_txt.text)


def parse_fed_data(text):
    '''returns an instance of FedData
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

    return FedData(
        data_version="",  # FIXME
        station_name=data["sites"]["Site"][0],
        station_code=data["sites"]["Code"][0],
        station_category="global",
        observation_category=(
            "Air sampling observation at a stationary platform"
        ),
        country_territory="",  # empty should be ok
        contributor=data["datasets"]["Dataset"][0].split(' ')[0].lower(),
        latitude=data["sites"]["Latitude"][0],
        longitude=data["sites"]["Longitude"][0],
        altitude=data["sites"]["Elevation"][0],
        nr_of_sampling_heights="1",
        sampling_heights="",  # empty should be ok
        contact_point="nmhyslop@ucdavis.edu",
        dataset=data["datasets"]["Dataset"][0],
        parameter=data["parameters"]["Parameter"][0],
        parameter_code=data["parameters"]["Code"][0],
        time_interval=data["datasets"]["Frequency"][0].lower(),
        measurement_unit=data["parameters"]["Units"][0].replace("Âµ", 'u'),
        measurement_method="",  # empty should be ok
        sampling_type="continuous",
        time_zone="UTC",
        measurement_scale="",  # empty should be ok
        status_flags=data["status flags"],
        data=data["data"]
    )
