import os
import pandas as pd
from collections import namedtuple


DATADIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


DATASETS = [
    {
        "name": "Precipitation",
        "href": "/catalog/dataset/1",
        "id": 1,
        "time_interval": "daily",
        "contact": "corinne.galy-lacaux@aero.obs-mip.fr",
    },
    {
        "name": "Gas",
        "href": "/catalog/dataset/2",
        "id": 2,
        "time_interval": "monthly",
        "contact": "corinne.galy-lacaux@aero.obs-mip.fr",
    },
    {
        "name": "Aerosols",
        "href": "/catalog/dataset/3",
        "id": 3,
        "time_interval": "daily",
        "contact": "corinne.galy-lacaux@aero.obs-mip.fr",
    },
    # Meteo dataset differs, it has different
    # id for different sites
    {
        "name": "Meteo",
        "href": "/catalog/dataset/4",
        "ids": [10, 11, 12, 13],
        "site_ids": [11, 12, 14, 13],
        "time_interval": "hourly",
        "contact": "Beatrice.Marticorena@lisa.u-pec.fr",
    },
]


SiteInfo = namedtuple(
    "SiteInfo",
    [
        "country",
        "site",
        "code",
        "classification",
        "latitude",
        "longitude",
        "altitude",
    ]
)


class InputError(Exception):
    pass


def get_all_parameters(dataset):
    parameter_file = os.path.join(
        DATADIR, "indaaf_parameters.csv"
    )
    df = pd.read_csv(parameter_file)
    df = df.loc[df['Theme'] == dataset]
    return list(df["Parameter name"].values)


def get_all_site_codes():
    return list(range(1, 17))


def get_dataset_id(dataset, site_id):
    if dataset == "Meteo":
        try:
            return DATASETS[3]["ids"][
                DATASETS[3]["site_ids"].index(site_id)
            ]
        except ValueError:
            print(
                "Meteo dataset is only available for "
                "sites 11, 12, 13, and 14"
            )
            raise(InputError)
    try:
        return DATASETS[
            [row["name"] for row in DATASETS].index(dataset)
        ]["id"]
    except ValueError:
        print("Unvalid datasets. Valid datasets:")
        print(DATASETS)
        raise(InputError)


def get_parameter_id(parameter, dataset):
    parameter_file = os.path.join(
        DATADIR, "indaaf_parameters.csv"
    )
    df = pd.read_csv(parameter_file)
    row = df.loc[
        (df['Parameter name'] == parameter) &
        (df['Theme'] == dataset)
    ]
    if row.empty:
        print("Unvalid parameter. Valid parameters:")
        print(df)
        raise(InputError)
    else:
        return row


def get_site_info(site_id):
    site_file = os.path.join(
        DATADIR, "indaaf_sites.csv"
    )
    df = pd.read_csv(site_file)
    row = df.loc[df['ID'] == site_id]
    if row.empty:
        print("Unvalid site ID. Valid sites:")
        print(df)
        raise(InputError)
    return SiteInfo(
        country=row["Location"].values[0],
        site=row["Site name"].values[0],
        code=str(row["ID"].values[0]),
        classification=row["Type"].values[0],
        latitude=row["Latitude (°)"].values[0],
        longitude=row["Longitude (°)"].values[0],
        altitude=row["Altitude (m)"].values[0],
    )
