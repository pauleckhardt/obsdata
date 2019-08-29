from datetime import date, datetime
import os
import pytest


from obsdata.fed_data import (
    set_request_data,
    parse_fed_data
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
    ("latitude", "43.74350"),
    ("longitude", "-101.94120"),
    ("altitude", "736"),
    ("parameter", "Carbon, Organic Total (Fine)"),
    ("parameter_code", "OCf"),
    ("measurement_unit", "ug/m^3 LC"),
))
def test_parse_metadata(fed_data, para, expect):
    data = parse_fed_data(fed_data)
    assert getattr(data, para) == expect


@pytest.mark.parametrize('parameter,row,expect', (
    ('datetime', 0, datetime(2017, 1, 1)),
    ('value', 0, 0.30555),
    ('status', 0, 8),
    ('nr_of_samples', 0, -999),
    ('datetime', 1, datetime(2017, 1, 4)),
    ('value', 1, 0.39832),
))
def test_parse_data(fed_data, parameter, row, expect):
    data = parse_fed_data(fed_data)
    assert getattr(data.records[row], parameter) == expect
