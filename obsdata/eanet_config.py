import os
from collections import namedtuple
import numpy as np


DATADIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


EanetSite = namedtuple(
    "EanetSite",
    [
        "country",
        "site",
        "code",
        "classification",
        "latitude",
        "longitude",
        "altitude"
    ]
)


Datasets = [{
    "name": "Wet Monthly",
    "id": 1,
    "parameters": [
        "SO2", "HNO3", "HCl", "NH3", "NO", "NO2",
        "NOx", "O3", "PM10", "PM25", "SO42-", "NO3-",
        "Cl-", "NH4+", "Na+", "K+", "Mg2+", "Ca2+"
    ]
}]


class InputError(Exception):
    pass


def coordinates_to_decimal_form(latitude, longitude):
    def get_decimal_value(x):
        integer_part = int(x.split('°')[0])
        arc_minutes = int(x.split('°')[1].split("'")[0])
        try:
            arc_seconds = int(x.split('°')[1].split("'")[1].split('"')[0])
        except ValueError:
            arc_seconds = 0
        return np.round(
            (integer_part + arc_minutes / 60 + arc_seconds / 3600),
            decimals=5
        )
    latitude_sign = 1 if latitude[-1] == "N" else -1
    longitude_sign = 1 if longitude[-1] == "E" else -1
    return (
        latitude_sign * get_decimal_value(latitude),
        longitude_sign * get_decimal_value(longitude)
    )


def get_site_information():
    eanetfile = os.path.join(DATADIR, 'eanet_sites.txt')
    with open(eanetfile, 'r') as sitefile:
        lines = sitefile.readlines()
        sites = []
        for index, line in enumerate(lines):
            sline = [i.strip() for i in line.split("  ") if not i == ""]
            if len(sline) == 1:
                country = sline[0]
            if index > 0 and len(sline) > 1:
                latitude, longitude = coordinates_to_decimal_form(
                    sline[3], sline[4]
                )
                try:
                    site = sline[0].split(" - ")[1]
                except IndexError:
                    site = sline[0]
                sites.append(EanetSite(
                    country=country,
                    site=site,
                    code=sline[1],
                    classification=sline[2],
                    latitude=latitude,
                    longitude=longitude,
                    altitude=sline[5]
                ))
    return sites


def validate_input(dataset_id, site_code, parameter):
    if dataset_id not in ['1']:
        print('Only dataset_id 1: "Dry Monthly" is implemented')
        raise(InputError)
    if parameter not in Datasets[0]["parameters"] and parameter != 'all':
        print("Dataset only contains the following parameters: {}".format(
            Datasets[0]["parameters"]
        ))
        raise(InputError)
    if site_code not in [s.code for s in eanet_sites] and site_code != 'all':
        print('no metadata is found for site {}.'.format(site_code))
        print('available sites are:')
        for site in eanet_sites:
            print(site)
        raise(InputError)
    return True


eanet_sites = get_site_information()
