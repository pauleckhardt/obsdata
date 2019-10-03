import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import namedtuple
from itertools import product

from obsdata.save_data import ObsData, Record, save_data_txt
from obsdata.eanet_config import eanet_sites


class EanetWetDataExtractor:

    def __init__(self, csvfile, parameter):
        self.parameter = parameter
        self.csvfile = csvfile
        table_locations = self._get_table_locations()
        index = self._get_first_table_with_target(table_locations)
        if index == -1:
            print("target data not found in file")
            exit(0)
        usecols = range(
            table_locations[index]["start"],
            table_locations[index]["end"]
        )
        self.df = pd.read_csv(csvfile, skiprows=9, usecols=usecols)

    def _get_table_locations(self):
        '''these csv files are non standard and typically
           contain six different tables, (i.e. one row of
           the csv file can contain data from six different
           tables), this function returns a dictionary
           describing the index of start and end column
           of each table
        '''
        # it is assumed that table names are found
        # on the second row of the csv file
        df = pd.read_csv(self.csvfile, skiprows=1)
        columns = [
            column for column in df.columns if not column.startswith("Unnamed")]
        table_locations = {}
        for index, column in enumerate(columns):
            table_locations[index] = {
                "name": column,
                "start": df.columns.tolist().index(column)
            }
            if index < len(columns) - 1:
                table_locations[index]["end"] = (
                    df.columns.tolist().index(columns[index + 1]) - 1
                )
            else:
                table_locations[index]["end"] = len(df.columns)
        return table_locations

    def _get_columns_in_table(self, start_column, end_column):
        """returns a list with data column headers"""
        # data column headers are assumed to be found on the 10th
        # row of the csv file
        df = pd.read_csv(
            self.csvfile,
            skiprows=9,
            usecols=range(start_column, end_column)
        )
        columns = [
            column for column in df.columns
            if not column.startswith("Unnamed")]

        return [
            column for column in columns
            if np.any([is_number(value) for value in df[column]])
        ]

    def _get_first_table_with_target(self, table_locations):
        """returns the index of the first table that contains
           data from the target, target data can be found in
           multiple tables"""
        for index in table_locations:
            for column in self._get_columns_in_table(
                    table_locations[index]["start"],
                    table_locations[index]["end"]):
                if column.startswith(self.parameter):
                    return index
        return -1

    def get_records(self):
        records = []
        for index in range(len(self.df[self.parameter])):
            if not self.df["Sample No."][index] > 0:
                continue
            records.append(
                Record(
                    start_datetime=self.get_date(index, "start"),
                    end_datetime=self.get_date(index, "end"),
                    value=self.get_value(index),
                    uncertainty=-999,
                    status=-999,
                    status_flag=-999,
                    nr_of_samples=-999,
                )
            )
        return records

    def get_value(self,index):
        value = float(self.df[self.parameter][index])
        if np.isnan(value):
            value = -999
        return value

    def get_date(self, row_index, start_or_end):
        offset = 0 if start_or_end == "start" else 2
        columns = self.df.columns.tolist()
        column_index = columns.index("Sampling period")
        return datetime.strptime(
            '{}T{}'.format(
                self.df[columns[column_index + offset]][row_index],
                self.df[columns[column_index + 1 + offset]][row_index]
            ),
            '%Y/%m/%dT%H:%M'
        )

    def get_unit(self):
        return self.df[self.parameter][1]


class EanetDryDataExtractor:

    def __init__(self, csvfile, parameter):
        self.csvfile = csvfile
        self.parameter = parameter
        self.df = pd.read_csv(csvfile, skiprows=1)

    def get_records(self):
        records = []
        if self.parameter not in self.df.columns:
            print("target not in products, available products:")
            print(self.get_products())
            return records
        for index in range(len(self.df[self.parameter])):
            records.append(
                Record(
                    start_datetime=self.get_start_date(index),
                    end_datetime=-999,
                    value=self.get_value(index),
                    uncertainty=-999,
                    status=-999,
                    status_flag=-999,
                    nr_of_samples=-999,
                )
            )
        return records

    def get_start_date(self, index):
        return datetime(
            self.df["Year"][index],
            self.df["Month"][index],
            self.df["Day"][index],
            self.df["Hour"][index]
        )

    def get_products(self):
        no_product = ["Country", "Site", "Year", "Month", "Day", "Hour", "Memo"]
        return [product for product in self.df.columns if product not in no_product]

    def get_unit(self):
        df = pd.read_csv(self.csvfile, nrows=2, header=None)
        return df[self.df.columns.tolist().index(self.parameter)][0]

    def get_value(self,index):
        value = float(self.df[self.parameter][index])
        if np.isnan(value):
            value = -999
        return value


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_payload(dataset, station_code, year):

    if dataset == "dry_deposition_auto":
        item_code = 2
    elif dataset == "dry_deposition_filter_pack":
        item_code = 3
    elif dataset == "dry_deposition_passive_sampler":
        item_code = 4
    elif dataset == "wet_deposition":
        item_code = 1

    # Country                           Code
    #
    # Cambodia                          KH
    # China                             CN
    # Indonesia                         ID
    # Japan                             JP
    # Korea, Republic of                KR
    # Lao People's Democratic Republic  LA
    # Malaysia                          MY
    # Mongolia                          MN
    # Myanmar                           MM
    # Philippines                       PH
    # Russia                            RU
    # Thailand                          TH
    # Viet Nam                          VN
    #
    # two first letter in station code is country code
    country_code = station[0:2]
    return {
        "mode": "download",
        "siteType": "1",
        "countryCd": country_code,
        "year": year,
        "siteCd": station_code,
        "itemCd": item_code,
    }



def download_csvfile(datadir, dataset, station, year):
    '''download file (if not already exists) and returns full filename'''

    url_base = "https://monitoring.eanet.asia"

    csvfile = os.path.join(
        datadir,
        "{}_{}_{}.csv".format(station, year, dataset)
    )

    if not os.path.exists(datadir):
        os.makedirs(datadir)

    if os.path.isfile(csvfile):
        return csvfile

    login_payload = {
        "email": "bengt.rydberg@molflow.com",
        "passwd": "M6R9XM9g",
        "submitBtn": "Sign+In",
    }

    payload = get_payload(dataset, station, year)

    with requests.Session() as session:
        p = session.post(url_base + "/document/signin/index", data=login_payload)
        # print the html returned or something more intelligent
        # to see if it's a successful login page.
        #
        # An authorised request.
        r = session.post(url_base + "/document/menu/index", data=payload)
        if "doctype html" in r.text:
            print('data not found')
            exit(0)

    with open(csvfile, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

    return csvfile


def get_data():

    csvfile = download_csvfile(datadir, dataset, station, year)

    if dataset == "wet_deposition":
        data_extractor = EanetWetDataExtractor(csvfile, parameter)
    else:
        data_extractor = EanetDryDataExtractor(csvfile, parameter)

    records = data_extractor.get_records()

    eanet_site = eanet_sites[
        [s.code for s in eanet_sites].index(station)
    ]

    return ObsData(
        data_version="?",
        station_name=eanet_site.site.replace('ñ', 'n'),
        station_code=eanet_site.code,
        station_category="global",
        observation_category=(
            "Air sampling observation at a stationary platform"),
        country_territory=eanet_site.country,
        contributor="eanet",
        latitude=eanet_site.latitude,
        longitude=eanet_site.longitude,
        altitude=eanet_site.altitude,
        nr_of_sampling_heights=1,
        sampling_heights="?",
        contact_point="?",
        dataset=dataset,
        parameter=parameter,
        parameter_code=parameter,
        time_interval="hourly",
        measurement_unit=data_extractor.get_unit(),
        measurement_method="?",
        sampling_type="continuous",
        time_zone="UTC",
        measurement_scale="?",
        status_flags="?",
        records=records,
    )


if __name__ == "__main__":

    datadir = '/home/bengt/Downloads/'
    parameters = ["SO42-", "nss-SO42-", "NO3-", "Cl-", "NH4+", "Na+", "K+", "Ca2+", "nss-Ca2+", "Mg2+", "H+", "pH", "EC"]
    parameter = 'SO42-'
    station = "CNA004"
    year = 2005
    # parameter = "SO2"
    dataset = "wet_deposition"
    # dataset = "dry_deposition_auto"

    obs_data = get_data()
    save_data_txt(datadir, obs_data)

