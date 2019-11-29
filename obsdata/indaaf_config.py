import os
import pandas as pd


DATADIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


datasets = [
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


class InputError(Exception):
    pass


def get_dataset_id(dataset, site_id):
    if dataset == "Meteo":
        try:
            return datasets[3]["ids"][
                datasets[3]["site_ids"].index(site_id)
            ]
        except ValueError:
            return 0
    try:
        return datasets[
            [row["name"] for row in datasets].index(dataset)
        ]["id"]
    except ValueError:
        print("Unvalid datasets. Valid datasets:")
        print(datasets)
        return 0


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
        print(df)
        raise(InputError)
    else:
        return row


def validate_site_id(site_id):
    site_file = os.path.join(
        DATADIR, "indaaf_sites.csv"
    )
    df = pd.read_csv(site_file)
    row = df.loc[df['ID'] == site_id]
    if row.empty:
        print("Unvalid site ID. Valid sites:")
        print(df)
        raise(InputError)
    return row
