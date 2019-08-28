from datetime import date, datetime
import os
import pytest
import numpy as np
from netCDF4 import Dataset, num2date


from obsdata.fed_data import (
    get_site_info,
    get_all_site_codes,
    get_parameter_info,
    set_request_data,
    parse_fed_data,
    save_data_txt,
    save_data_netcdf,
    validate_input,
    InputError
)


@pytest.fixture
def fed_data():
    datafile = os.path.join(os.path.dirname(__file__), "data.txt")
    with open(datafile, mode='r') as file:
        return file.read()


@pytest.fixture
def expected_output_file():
    datafile = os.path.join(
        os.path.dirname(__file__),
        "badl1_ocf_20170101.dat"
    )
    with open(datafile, mode='r') as file:
        return file.read()


@pytest.fixture
def tmp_dir(tmpdir):
    return tmpdir.mkdir("sub")


@pytest.fixture
def netcdf_dataset(fed_data, tmp_dir):
    data = parse_fed_data(fed_data)
    save_data_netcdf(tmp_dir, data)
    return Dataset(
        tmp_dir.join("badl1.improve.as.cs.ocf.nl.da.nc"),
        "r"
    )


def test_validate_input_not_raises():
    assert validate_input('improve aerosol', 'BADL1', 'OCf')


@pytest.mark.parametrize('dataset,site,parameter', (
    ('no improve aerosol', 'BADL1', 'OCf'),
    ('improve aerosol', 'ReallyBADL1', 'OCf'),
    ('improve aerosol', 'BADL1', 'LCHF'),
))
def test_validate_input_raises(dataset, site, parameter):
    with pytest.raises(InputError):
        validate_input(dataset, site, parameter)


@pytest.mark.parametrize('site_code,expect', (
    ('ACAD1', '1'),
    ('BADL1', '59'),
))
def test_get_site_info(site_code, expect):
    site_info = get_site_info("improve aerosol", site_code)
    assert site_info["ID"] == expect


@pytest.mark.parametrize('dataset,parameter_code,expect', (
    ('improve aerosol', 'ECf', '114'),
    ('improve aerosol', 'OCf', '141'),
    ('castnet', 'O3', '201'),
))
def test_get_parameter_info(dataset, parameter_code, expect):
    parameter_info = get_parameter_info(dataset, parameter_code)
    assert parameter_info["ParameterID"] == expect


def test_get_all_site_codes():
    site_codes = get_all_site_codes("improve aerosol")
    assert (
        len(site_codes) == 224 and
        site_codes[0] == 'ACAD1' and
        site_codes[-1] == 'ZICA1'
    )


def test_set_request_data_date():
    dataset_id = 10001
    site_id = 1
    parameter_id = 114
    df = "Daily"
    start_date = date(2017, 1, 1)
    end_date = date(2017, 1, 31)
    request_data = set_request_data(
        dataset_id, site_id, parameter_id, df, start_date, end_date)
    assert (
        request_data["dsidse"] == dataset_id and
        request_data["dt"] == "2017/01/01>2017/01/31" and
        request_data["siidse"] == site_id and
        request_data["paidse"] == parameter_id and
        request_data["df"] == df
    )


@pytest.mark.parametrize('para,expect', (
    ("time_interval",  "daily"),
    ("station_name", "Badlands NP"),
    ("station_code", "BADL1"),
    ("dataset", 'IMPROVE Aerosol'),
    ("country_territory", "SD"),
    ("latitude", "43.74350"),
    ("longitude", "-101.94120"),
    ("altitude", "736"),
    ("parameter", "Carbon, Organic Total (Fine)"),
    ("parameter_code", "OCf"),
    ("measurement_unit", "µg/m^3 LC"),
))
def test_parse_metadata(fed_data, para, expect):
    data = parse_fed_data(fed_data)
    assert data[para] == expect


@pytest.mark.parametrize('parameter,row,expect', (
    ('Dataset', 0, 'IMPFSPED'),
    ('SiteCode', 0, 'BADL1'),
    ('POC', 0, '1'),
    ('Date', 0, datetime(2017, 1, 1)),
    (':Value', 0, '0.30555'),
    ('Dataset', 1, 'IMPFSPED'),
    ('SiteCode', 1, 'BADL1'),
    ('POC', 1, '1'),
    ('Date', 1, datetime(2017, 1, 4)),
    (':Value', 1, '0.39832'),
))
def test_parse_data(fed_data, parameter, row, expect):
    data = parse_fed_data(fed_data)
    assert data["data"][parameter][row] == expect


def test_save_data_txt(fed_data, tmp_dir, expected_output_file):
    data = parse_fed_data(fed_data)
    save_data_txt(tmp_dir, data)
    outfile = tmp_dir.join("badl1.improve.as.cs.ocf.nl.da.dat")
    with open(outfile, mode='r') as file:
        assert file.read() == expected_output_file


def test_save_netcdf_attribute(netcdf_dataset):
    assert (
        netcdf_dataset.station_name == "Badlands NP"
        and netcdf_dataset.latitude == 43.74350
        and netcdf_dataset.longitude == -101.94120
        and netcdf_dataset.altitude == 736.0
    )


def test_save_netcdf_data(netcdf_dataset):
    expected_data = np.array([
        0.30555, 0.39832, 0.49467, 0.65754, 0.85112, 0.48262,
        0.77864, 0.43116, 0.17473, 0.21264, 0.21017
    ])
    assert np.all(netcdf_dataset["OCf"] == expected_data)


def test_save_netcdf_datetime(netcdf_dataset):
    expected_dates = np.array([
        datetime(2017, 1, 1, 0, 0),
        datetime(2017, 1, 4, 0, 0),
        datetime(2017, 1, 7, 0, 0),
        datetime(2017, 1, 10, 0, 0),
        datetime(2017, 1, 13, 0, 0),
        datetime(2017, 1, 16, 0, 0),
        datetime(2017, 1, 19, 0, 0),
        datetime(2017, 1, 22, 0, 0),
        datetime(2017, 1, 25, 0, 0),
        datetime(2017, 1, 28, 0, 0),
        datetime(2017, 1, 31, 0, 0)
    ])
    dates = [
        num2date(
            time,
            netcdf_dataset["time"].units,
            netcdf_dataset["time"].calendar
        )
        for time in netcdf_dataset["time"]
    ]
    assert np.all(dates == expected_dates)
