import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import numpy as np
from obsdata.eanet_config import eanet_sites
from obsdata.save_data import (
    save_data_txt, ObsData, Record
)


class EanetSheetExtractor:

    def __init__(self, sheet):
        self.sheet = sheet

    def locate_variable(self, variable):
        '''returns the position where the variable can be
           found in the sheet
        '''
        row = -1
        column = -1
        for col_index, col in enumerate(self.sheet.columns):
            for row_index, value in enumerate(self.sheet[col]):
                if value == variable:
                    row = row_index
                    column = col_index
                    break
        return (row, column)

    def get_unit(self):
        '''returns the units of the measurements'''
        try:
            return self.sheet.loc[1][0].split("：")[1].strip()
        except IndexError:
            try:
                return self.sheet.loc[1][0].split(":")[1].strip()
            except IndexError:
                return "?"

    def get_year(self):
        '''returns the year'''
        return int(self.sheet.loc[1][3])

    def get_sites(self):
        '''returns a dictionary where each item describes where
           data from a site can be found in the sheet
        '''
        (row_site, column_site) = self.locate_variable("Site")
        stations = {}
        counter = 0
        for index, value in enumerate(
                self.sheet[self.sheet.columns[column_site]]):
            if index > row_site and pd.notnull(value):
                if value.startswith('(') or value.endswith(')'):
                    # if comments below site name
                    continue
                stations[counter] = {
                    "site": value.strip().replace('1', ''),
                    "row_start": index,
                    "row_end": index + 3,
                    "column": column_site,
                }
                counter += 1
        return stations

    def get_records(self, site):
        '''returns the records of a given site
           (monthly average data)'''
        headers = []
        records_no_date = []
        for row in range(site["row_start"], site["row_end"] + 1):
            headers.append(self.sheet.loc[row][site["column"] + 1])
            start_index = site["column"] + 2
            record = []
            # loop over 12 months
            for d in self.sheet.loc[row][start_index : start_index + 12]:
                try:
                    record.append(float(d))
                except ValueError:
                    record.append(-999)
            records_no_date.append(record)
        records_no_date = np.array(records_no_date).transpose().tolist()
        # add date to records
        headers = ["date"] + headers
        year = self.get_year()
        records = []
        for index, record in enumerate(records_no_date):
            if record[2] != -999 and record[3] != -999:
                uncertainty = (record[2] - record[3]) / 2
            else:
                uncertainty = -999
            records.append(Record(
                datetime=datetime(year, index + 1, 1),
                value=record[0],
                uncertainty=uncertainty,
                status=-999,
                status_flag=-999,
                nr_of_samples=-999,
            ))
        return (headers, records)


def get_all_sites(list_of_sheets):
    '''returns an array of the name all sites'''
    list_of_sites = []
    for sheet in list_of_sheets:
        sheet_extractor = EanetSheetExtractor(sheet)
        sites = sheet_extractor.get_sites()
        for site in sites:
            list_of_sites.append(sites[site]["site"])
    return np.unique(list_of_sites)


def merge_data(list_of_sheets, eanet_site, dataset, parameter):
    '''merge data from many years and returns an instance of EanetData'''
    records = []
    for sheet in list_of_sheets:
        sheet_extractor = EanetSheetExtractor(sheet)
        sites = sheet_extractor.get_sites()
        for site in sites:
            if not sites[site]["site"] == eanet_site.site:
                continue
            _, current_records = sheet_extractor.get_records(
                sites[site])
            for record in current_records:
                records.append(record)
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
        time_interval="monthly",
        measurement_unit=sheet_extractor.get_unit(),
        measurement_method="?",
        sampling_type="continuous",
        time_zone="UTC",
        measurement_scale="?",
        status_flags="?",
        records=records,
    )


def get_datafile_url(year, dataset):
    '''returns an url from where the excel file can be downloaded'''
    available_datasets = [
        "Dry Monthly",
        "Inland Annual",
        "Soil and Vegetation",
        "Wet Annual",
        "Wet Monthly",
        "Catchment",
    ]
    if dataset not in available_datasets:
        print("dataset is not available")
        exit(0)
    available_years = range(2000, 2018)
    if year not in available_years:
        print("year is not available")
        exit(0)

    url_base = "https://monitoring.eanet.asia"
    r = requests.get(url_base + "/document/public")

    soup = BeautifulSoup(r.content, 'html.parser')
    view = soup.find("div", {"id": "view-{}".format(year)})
    links = view.find_all('a')
    for link in links:
        href = link.get('href')
        tag1 = link.find_all("span", {"class": "link_xlsx"})
        tag2 = link.find_all("span", {"class": "link_xls"})
        if tag1:
            tag = tag1[0]
        elif tag2:
            tag = tag2[0]
        else:
            continue
        if tag.text.strip().startswith(dataset):
            return url_base + href


def retrieve_file(url, datadir, dataset, year):
    '''download file (if not already exists) and returns full filename'''
    xlsfile = os.path.join(
        datadir, '{}-{}.xls'.format(dataset, year))
    print(os.path.isfile(xlsfile))
    if not os.path.isfile(xlsfile):
        r = requests.get(url, stream=True)
        with open(xlsfile, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    return xlsfile


def get_xlsfiles(datadir, dataset, start_year, end_year):
    '''returns a list of filenames of the dataset,
       download datafiles in not locally available
    '''
    xlsfiles = []
    for year in range(start_year, end_year + 1):
        xlsfile = os.path.join(
            datadir, '{}-{}.xls'.format(dataset, year))
        if not os.path.isfile(xlsfile):
            url = get_datafile_url(year, dataset)
            retrieve_file(url, datadir, dataset, year)
        xlsfiles.append(xlsfile)
    return xlsfiles


if __name__ == "__main__":

    start_year = 2001
    end_year = 2017
    dataset = "Dry Monthly"
    parameter = "SO2"
    download = False
    datadir = "/home/bengt/Downloads/eanet/"
    outdir = "/tmp"

    xlsfiles = get_xlsfiles(datadir, dataset, start_year, end_year)

    # for these sites we have needed meta data
    list_of_eanet_sites = np.array([s.site for s in eanet_sites])

    list_of_sheets = [
        pd.read_excel(xlsfile, sheet_name=parameter)
        for xlsfile in xlsfiles
    ]

    # sheets = pd.read_excel(xlsfile, sheet_name=None).keys()
    list_of_sites_all_sheets = get_all_sites(list_of_sheets)
    for site in list_of_sites_all_sheets:

        if not np.any(list_of_eanet_sites == site):
            # if we not have meta data for this site
            continue

        eanet_site = eanet_sites[
            np.nonzero(list_of_eanet_sites == site)[0][0]]

        eanet_data = merge_data(
            list_of_sheets, eanet_site, dataset, parameter)

        save_data_txt(outdir, eanet_data)
