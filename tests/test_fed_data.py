from datetime import date
import os
import pytest

from obsdata.fed_data import (
    get_site_info,
    get_all_site_codes,
    get_parameter_info,
    set_request_data,
    parse_fed_data,
    save_data
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


@pytest.mark.parametrize('site_code,expect', (
    ('ACAD1', '1'),
    ('BADL1', '59'),
))
def test_get_site_info(site_code, expect):
    site_info = get_site_info(site_code)
    assert site_info["ID"] == expect


@pytest.mark.parametrize('parameter_code,expect', (
    ('ECf', '114'),
    ('OCf', '141'),
))
def test_get_parameter_info(parameter_code, expect):
    parameter_info = get_parameter_info(parameter_code)
    assert parameter_info["ParameterID"] == expect


def test_get_all_site_codes():
    site_codes = get_all_site_codes()
    assert (
        len(site_codes) == 224 and
        site_codes[0] == 'ACAD1' and
        site_codes[-1] == 'ZICA1'
    )


def test_set_request_data_date():
    site_id = 1
    parameter_id = 114
    start_date = date(2017, 1, 1)
    end_date = date(2017, 1, 31)
    request_data = set_request_data(
        site_id, parameter_id, start_date, end_date)
    assert (
        request_data["dt"] == "2017/01/01>2017/01/31" and
        request_data["siidse"] == site_id and
        request_data["paidse"] == parameter_id
    )


@pytest.mark.parametrize('para,expect', (
    ("frequency",  "Daily"),
    ("site", "Badlands NP"),
    ("site_code", "BADL1"),
    ("dataset", "IMPFSPED"),
    ("state", "SD"),
    ("county", "46071"),
    ("latitude", "43.74350"),
    ("longitude", "-101.94120"),
    ("elevation", "736"),
    ("start_date", "03/02/1988"),
    ("end_date", "11/28/2018"),
    ("num_pocs", "1"),
    ("dataset_id", "10001"),
    ("parameter", "Carbon, Organic Total (Fine)"),
    ("parameter_code", "OCf"),
    ("aqs_code", "88320"),
    ("units", "µg/m^3 LC"),
))
def test_parse_metadata(fed_data, para, expect):
    data = parse_fed_data(fed_data)
    assert data[para] == expect


@pytest.mark.parametrize('row,expect', (
    (0, ['Dataset', 'SiteCode', 'POC', 'Date', ':Value']),
    (1, ['IMPFSPED', 'BADL1', '1', date(2017, 1, 1), '0.30555']),
    (2, ['IMPFSPED', 'BADL1', '1', date(2017, 1, 4), '0.39832']),
))
def test_rawdata(fed_data, row, expect):
    data = parse_fed_data(fed_data)
    assert data["data"][row] == expect


def test_save_data(fed_data, expected_output_file):

    data = parse_fed_data(fed_data)
    outdir = "/tmp"
    filename = "badl1_ocf_20170101.dat"
    os.remove(os.path.join(outdir, filename))
    save_data(outdir, data)
    with open(os.path.join(outdir, filename), mode='r') as file:
        assert file.read() == expected_output_file
