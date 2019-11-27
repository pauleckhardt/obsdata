import os
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from obsdata.save_data import ObsData, Record


url_base = "https://indaaf.sedoo.fr"
login_url = url_base + "/j_spring_security_check"
datadir = "/tmp"


def get_login_payload():
    """returns login payload"""
    indaaf_configfile = os.path.join(os.environ['HOME'], '.indaafconfig')
    if not os.path.isfile(indaaf_configfile):
        print(
            'You need to create an indaaf config file with credentials.\n' +
            'Check the README file for instructions!'
        )
        exit(1)
    with open(indaaf_configfile) as json_file:
        login_data = json.load(json_file)
    return {
        "username": login_data["user"],
        "password": login_data["password"],
        "submit": "Ok",
    }


def get_csv_file(
        dataset_id, site_id, parameter_id, out_filename):
    """retrieves a csv file form indaaf and returns True
       or False on success or failure"""
    login_payload = get_login_payload()

    requests.packages.urllib3.disable_warnings(
        category=InsecureRequestWarning)

    with requests.Session() as session:
        p = session.post(
            login_url,
            data=login_payload,
            verify=False
        )
        if "Create an account" in p.text:
            print(
                'not able to login on {},\n'.format(login_url) +
                'is your credentials valid?'
            )
            exit(0)

        url_download = url_base + "/download/{}/{}/{}".format(
            dataset_id, site_id, parameter_id
        )

        r = session.get(url_download, verify=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        link = soup.find("a", id="dl_button_1")
        try:
            href = link.get('href')
        except AttributeError:
            print("Data not available.")
            return False
        url_download_csv = url_base + href
        r = session.get(url_download_csv)
        # save csvdata locally
        with open(out_filename, 'wb') as f:
            for chunk in r.iter_content():
                chunk = chunk.replace(b'\x83', b'')
                chunk = chunk.replace(b'\xCA', b'u')
                f.write(chunk)
        return True


def get_site_info(site_id):
    """scrapes an indaaf web-page on site info"""
    login_payload = get_login_payload()

    url_site = url_base + "/catalog/site/{}".format(site_id)
    requests.packages.urllib3.disable_warnings(
        category=InsecureRequestWarning)

    with requests.Session() as session:
        session.post(
            login_url, data=login_payload, verify=False)
        r = session.get(url_site)

        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all("table")
        data = []
        for row in table[0].findAll("tr"):
            try:
                cols = [ele.text.strip() for ele in row]
                data.append(cols)
            except AttributeError:
                pass
        for row in table[1].findAll("tr"):
            try:
                cols = [ele.text.strip() for ele in row]
                data.append(cols)
            except AttributeError:
                pass
        headers = [row[0] for row in data]
        values = [row[1] for row in data]
    return headers, values


def create_indaaf_sites_file():
    """creates a csv file that describes indaaf sites
    """
    data = {}
    nr_indaaf_sites = 16
    for index, site_id in enumerate(
            range(1, nr_indaaf_sites + 1)):
        headers, values = get_site_info(site_id)
        if index == 0:
            for header in headers:
                data[header] = []
            data["ID"] = []
        data["ID"].append(site_id)
        for header, value in zip(headers, values):
            data[header].append(value)
    df_out = pd.DataFrame(data, columns=data.keys())
    df_out.to_csv(
        os.path.join(datadir, 'indaaf_sites.csv'),
        index=None,
        header=True
    )


def get_parameter_info(parameter_id):
    """scrapes an indaaf web-page on parameter info"""
    login_payload = get_login_payload()

    url_parameter = url_base + "/catalog/param/{}".format(
        parameter_id)

    with requests.Session() as session:
        session.post(
            login_url, data=login_payload, verify=False)
        r = session.get(url_parameter)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all("table")
        data = []
        for row in table[0].findAll("tr"):
            try:
                cols = [ele.text.strip() for ele in row]
                data.append(cols)
            except AttributeError:
                pass
        headers = [row[0] for row in data]
        values = [row[1] for row in data]
    return headers, values


def create_indaaf_parameters_file():
    """creates a csv file that describes indaaf parameters
    """
    data = {}
    nr_indaaf_parameters = 53
    for index, parameter_id in enumerate(
            range(1, nr_indaaf_parameters + 1)):
        headers, values = get_parameter_info(parameter_id)
        if index == 0:
            for header in headers:
                data[header] = []
            data["ID"] = []
        data["ID"].append(parameter_id)
        for header, value in zip(headers, values):
            data[header].append(value)
    data.pop('Code')  # not all parameters have this
    df_out = pd.DataFrame(data, columns=data.keys())
    df_out.to_csv(
        os.path.join(datadir, 'indaaf_parameters.csv'),
        index=None,
        header=True
    )


def get_records(
        csv_file, parameter, site_info, parameter_info, dataset_info):
    """parse indaaf csv file and returns an instance of ObsData
    """
    df = pd.read_csv(csv_file, skiprows=19, delimiter=';')
    records = []
    target_parameter = df.columns[1]
    for _, row in df.iterrows():
        try:
            start_datetime = datetime.strptime(
                    row["Date"], "%Y-%m-%d")
        except ValueError:
            start_datetime = datetime.strptime(
                    row["Date"], "%Y-%m-%d %H:%M:%S")
        records.append(
            Record(
                start_datetime=start_datetime,
                end_datetime=-9999,
                value=row[target_parameter],
                uncertainty=-999,
                status=-999,
                status_flag=-999,
                nr_of_samples=-999,
            )
        )
    return ObsData(
        data_version="?",
        station_name=site_info["Site name"].values[0],
        station_code=str(site_info["ID"].values[0]),
        station_category="global",
        observation_category=(
            "Air sampling observation at a stationary platform"),
        country_territory=site_info["Location"].values[0],
        contributor="indaaf",
        latitude=site_info["Latitude (°)"].values[0],
        longitude=site_info["Longitude (°)"].values[0],
        altitude=site_info["Altitude (m)"].values[0],
        nr_of_sampling_heights=1,
        sampling_heights="?",
        contact_point=dataset_info["contact"],
        dataset=parameter_info["Theme"].values[0],
        parameter=parameter,
        parameter_code=parameter,
        time_interval=dataset_info["time_interval"],
        measurement_unit=parameter_info[
            "Unit"].values[0].replace(
                '°', 'degrees ').replace(
                    'µ', 'u'),
        measurement_method="?",
        sampling_type="continuous",
        time_zone="UTC",
        measurement_scale="?",
        status_flags="?",
        records=records,
    )


def date_filter_records(date_start, date_end, records):
    """filter records on time"""
    start_datetimes = np.array(
        [record.start_datetime for record in records]
    )
    indexes = np.nonzero(
        (start_datetimes >= date_start) &
        (start_datetimes < date_end)
    )[0]
    return [records[index] for index in indexes]
