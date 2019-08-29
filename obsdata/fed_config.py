import os
import pkg_resources
import csv
from collections import namedtuple


DATADIR = pkg_resources.resource_filename(__name__, "")


datasets = {
    "improve aerosol": {
        "id": 10001,
        "time_interval": "Daily",
        "site_file": os.path.join(DATADIR, "fedsites_improve_aerosol.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_improve_aerosol.csv"),
    },
    # castnet ozone hourly
    "castnet": {
        "id": 23005,
        "time_interval": "Hourly",
        "site_file": os.path.join(DATADIR, "fedsites_castnet.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_castnet.csv"),
    }
}


SiteInfo = namedtuple(
    "SiteInfo",
    [
        "id",
        "code",
        "name",
        "country",
        "state",
        "latitude",
        "longitude",
        "elevation",
        "start",
        "end",
    ]
)


ParameterInfo = namedtuple(
    "ParameterInfo", ["id", "code", "name"]
)


class InputError(Exception):
    pass


def get_site_info(dataset, site_code):
    '''returns an instance of SiteInfo with data
       as contained in the site file
    '''
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] == site_code:
                return SiteInfo(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    country=row[3],
                    state=row[4],
                    latitude=row[6],
                    longitude=row[7],
                    elevation=row[8],
                    start=row[9],
                    end=row[10],
                )
    print("site_code {0} not found for dataset {1}".format(
        site_code, dataset))
    raise(InputError)


def get_all_site_codes(dataset):
    '''returns a list containing all site codes
       (e.g. BADL1)
       of the site file of the dataset
    '''
    site_codes = []
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count > 0:
                site_codes.append(row[1])
    return site_codes


def get_parameter_info(dataset, parameter_code):
    '''returns an instance of ParameterInfo
       as defined by the parameter file
    '''
    with open(datasets[dataset]["parameter_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2] == parameter_code:

                return ParameterInfo(
                    id=row[3],
                    code=row[2],
                    name=row[1]
                )
    print("parameter_code {0} not found for dataset {1}".format(
        parameter_code, dataset))
    raise(InputError)


def validate_input(dataset, site, parameter):
    '''checks that input is valid'''
    # dataset
    if dataset not in datasets.keys():
        print(
            'dataset {} is not implemented.\n'.format(dataset) +
            'implemented datasets are:'
        )
        for dataset in datasets.keys():
            print("'{}'".format(dataset))
        raise(InputError)

    # get_site_info raises if site not found
    get_site_info(dataset, site)

    # get_parameter_info raises if site not found
    get_parameter_info(dataset, parameter)

    return True
