import os
import pandas as pd
from collections import namedtuple


DATADIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


DATASETS = [
    {
        "name": "CAPMoN_Ozone",
        "parameters": ["O3"],
        "baseurl": "http://donnees.ec.gc.ca/data/air/monitor/monitoring-of-atmospheric-gases/ground-level-ozone/",  # noqa
        "file_pattern": "AtmosphericGases-GroundLevelOzone-CAPMoN-AllSites-{year}.csv",  # noqa
        "year_start": 1988,
        "time_interval": "hourly",
    },
    {
        "name": "CAPMoN_Precip_Chemistry",
        "parameters": [
            'Ca2+',
            'Cl-',
            'H+',
            'K+',
            'Mg2+',
            'NH4+',
            'NO3-',
            'Na+',
            'SO42-',
            'nss-SO42-'
            'pH'
        ],
        "baseurl": "http://donnees.ec.gc.ca/data/air/monitor/monitoring-of-atmospheric-precipitation-chemistry/major-ions/",  # noqa
        "file_pattern": "AtmosphericPrecipitationChemistry-MajorIons-CAPMoN-AllSites-{year}.csv",  # noqa
        "year_start": 1983,
        "time_interval": "daily"
    }
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
        "sampling_heights",
    ]
)


class InputError(Exception):
    pass


def get_all_site_codes(dataset):
    site_file = os.path.join(
        DATADIR, "{}_sites.csv".format(dataset.lower())
    )
    df = pd.read_csv(site_file)
    return list(df["SiteID"].values)


def get_all_parameters(dataset):
    index = [ds["name"] for ds in DATASETS].index(dataset)
    return DATASETS[index]["parameters"]


def get_site_info(dataset, site_id):
    site_file = os.path.join(
        DATADIR, "{}_sites.csv".format(dataset.lower())
    )
    df = pd.read_csv(site_file)
    row = df.loc[df['SiteID'] == site_id]
    if row.empty:
        print("Unvalid site ID. Valid sites:")
        print(df[[
            "SiteID", "SiteName", "CountryCode", "SiteLandUse",
            "Latitude_deg", "Longitude_deg", "GroundElevAMSL_m"
        ]])
        raise(InputError)
    try:
        sampling_heights = row["SamplingHeightAG"].values[0]
    except KeyError:
        sampling_heights = "?"

    return SiteInfo(
        country=row["CountryCode"].values[0],
        site=row["SiteName"].values[0],
        code=row["SiteID"].values[0],
        classification=row["SiteLandUse"].values[0],
        latitude=row["Latitude_deg"].values[0],
        longitude=row["Longitude_deg"].values[0],
        altitude=row["GroundElevAMSL_m"].values[0],
        sampling_heights=sampling_heights,
    )


def validate_dataset(dataset):
    try:
        [ds["name"] for ds in DATASETS].index(dataset)
    except ValueError:
        print("{} is not a valid dataset.".format(dataset))
        print("The following datasets are handled:")
        print([ds["name"] for ds in DATASETS])
        raise(InputError)
    return True


def validate_parameter(dataset, parameter):
    index = [ds["name"] for ds in DATASETS].index(dataset)
    try:
        DATASETS[index]["parameters"].index(parameter)
    except ValueError:
        print("{} is not a valid parameter for dataset {}.".format(
            parameter, dataset))
        print("The following parameters are handled:")
        print(DATASETS[index]["parameters"])
        raise(InputError)
    return True
