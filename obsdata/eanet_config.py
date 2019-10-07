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


Datasets = [
    {
        "name": "wet_monthly",
        "id": 1,
        "parameters": [
            "Ca2+",
            "Cl-",
            "HCl",
            "HNO3",
            "K+",
            "Mg2+",
            "Na+",
            "NH3",
            "NH4+",
            "NO",
            "NOx",
            "NO2",
            "NO3-",
            "O3",
            "PM10",
            "PM25",
            "SO2",
            "SO42-",
        ],
    },
    {
        "name": "wet_deposition",
        "id": 2,
        "parameters": [
            'Anion',
            'Cation',
            'Ca2+',
            'CH3COO-',
            'Cl-',
            'C+A',
            'EC',
            'F-',
            'HCOO-',
            'HCO3-',
            'H+',
            'K+',
            'Mg2+',
            'Na+',
            'NH4+',
            'NO3-',
            'nss-Ca2+',
            'nss-SO42-',
            'pH',
            'PO43-',
            'Req.R1',
            'Req.R2',
            'R1',
            'R2',
            'SO42-',
        ]
    },
    {
        "name": "dry_deposition_auto",
        "id": 3,
        "parameters": [
            "NO",
            "NO2",
            "NOx*",
            "O3",
            "PM10",
            "PM2.5",
            "SO2"
        ],
    },
    {
        "name": "dry_deposition_filter_pack",
        "id": 4,
        "parameters": [
            'Ca2+',
            'Cl-',
            'HCl',
            'HNO3',
            'K+',
            'Mg2+',
            'Na+',
            'NH3',
            'NO3-',
            'NH4+',
            'SO2',
            'SO42-',
        ],
    },
    {
        "name": "dry_deposition_passive_sampler",
        "id": 5,
        "parameters": [
            'SO2',
            'NO2'
        ],
    }
]


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
    if int(dataset_id) not in [dataset["id"] for dataset in Datasets]:
        print('Only the following datasets are implemented:')
        for dataset in Datasets:
            print('{}: {}'.format(dataset["id"], dataset["name"]))
        raise(InputError)
    index = [dataset["id"] for dataset in Datasets].index(int(dataset_id))
    if parameter not in Datasets[index]["parameters"] and parameter != 'all':
        print("Dataset only contains the following parameters: {}".format(
            Datasets[index]["parameters"]
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
