from datetime import datetime
import os
import pytest
import numpy as np
from netCDF4 import Dataset, num2date

from obsdata.save_data import (
    save_data_txt,
    save_data_netcdf
)
from obsdata.fed_data import parse_fed_data


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
