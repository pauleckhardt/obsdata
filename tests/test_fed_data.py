from datetime import date
import pytest

from obsdata.fed_data import (
    get_site_info,
    get_all_site_codes,
    get_parameter_info,
    set_request_data
)


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
