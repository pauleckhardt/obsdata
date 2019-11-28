import os
import pandas as pd


DATADIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data"
)


datasets = [
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


def validate_site_id(dataset, site_id):
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
        exit(0)
    return row


def validate_dataset(dataset):
    try:
        [ds["name"] for ds in datasets].index(dataset)
    except ValueError:
        print("{} is not a valid dataset.".format(dataset))
        print("The following datasets are handled:")
        print([ds["name"] for ds in datasets])
        exit(0)


def validate_parameter(dataset, parameter):
    index = [ds["name"] for ds in datasets].index(dataset)
    try:
        datasets[index]["parameters"].index(parameter)
    except ValueError:
        print("{} is not a valid parameter for dataset {}.".format(
            parameter, dataset))
        print("The following parameters are handled:")
        print(datasets[index]["parameters"])
        exit(0)
