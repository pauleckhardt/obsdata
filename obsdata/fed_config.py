import os
import pkg_resources
import csv


DATADIR = pkg_resources.resource_filename(__name__, "")


datasets = {
    "improve aerosol": {
        "id": 10001,
        "df": "Daily",
        "site_file": os.path.join(DATADIR, "fedsites_improve_aerosol.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_improve_aerosol.csv"),
    },
    # castnet ozone hourly
    "castnet": {
        "id": 23005,
        "df": "Hourly",
        "site_file": os.path.join(DATADIR, "fedsites_castnet.csv"),
        "parameter_file": os.path.join(DATADIR, "dataset_castnet.csv"),
    }
}


class InputError(Exception):
    pass


def get_site_info(dataset, site_code):
    '''returns a dict with information of the site
       as contained in the site file
    '''
    site_info = {}
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                header = row
            else:
                if row[1] == site_code:
                    for item, value in zip(header, row):
                        site_info[item] = value
    return site_info


def get_all_site_codes(dataset):
    '''returns a list of containing all site codes
       (e.g. BADL1)
       within the site file of the dataset
    '''
    site_codes = []
    with open(datasets[dataset]["site_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count > 0:
                site_codes.append(row[1])
    return site_codes


def get_parameter_info(dataset, parameter_code):
    '''returns a dict with information of the parameter
       as defined by the parameter file
    '''
    parameter_info = {}
    with open(datasets[dataset]["parameter_file"]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                header = row
            else:
                if row[2] == parameter_code:
                    for item, value in zip(header, row):
                        parameter_info[item] = value
    return parameter_info


def validate_input(dataset, site, parameter):

    # dataset
    if dataset not in datasets.keys():
        print(
            'dataset {} is not implemented.\n'.format(dataset) +
            'implemented datasets are:'
        )
        for dataset in datasets.keys():
            print("'{}'".format(dataset))
        raise(InputError)

    # site
    site_info = get_site_info(dataset, site)
    if not site_info:
        print(
            'site-code {} is not available.\n'.format(site) +
            'available sites are:'
        )
        site_codes = get_all_site_codes(dataset)
        for site_code in site_codes:
            site_info = get_site_info(dataset, site_code)
            print("{}: {}".format(site_code, site_info))
        raise(InputError)

    # parameter
    parameter_info = get_parameter_info(dataset, parameter)
    if not parameter_info:
        print(
            'parameter-code {} is not available.\n'.format(parameter) +
            'available parameters are:'
        )
        with open(datasets[dataset]["parameter_file"]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print(row)
        raise(InputError)

    return True
