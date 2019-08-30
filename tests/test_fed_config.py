import pytest


from obsdata.fed_config import (
    get_site_info,
    get_all_site_codes,
    get_parameter_info,
    validate_input,
    InputError
)


def test_validate_input_not_raises():
    assert validate_input('10001', 'BADL1', 'OCf')


@pytest.mark.parametrize('dataset,site,parameter', (
    ('-99999', 'BADL1', 'OCf'),
    ('10001', 'ReallyBADL1', 'OCf'),
    ('10001', 'BADL1', 'LCHF'),
))
def test_validate_input_raises(dataset, site, parameter):
    with pytest.raises(InputError):
        validate_input(dataset, site, parameter)


@pytest.mark.parametrize('site_code,expect', (
    ('ACAD1', '1'),
    ('BADL1', '59'),
))
def test_get_site_info(site_code, expect):
    site_info = get_site_info("10001", site_code)
    assert getattr(site_info, "id") == expect


@pytest.mark.parametrize('dataset,parameter_code,expect', (
    ('10001', 'ECf', '114'),
    ('10001', 'OCf', '141'),
    ('23005', 'O3', '201'),
))
def test_get_parameter_info(dataset, parameter_code, expect):
    info = get_parameter_info(dataset, parameter_code)
    assert getattr(info, "id") == expect


def test_get_all_site_codes():
    site_codes = get_all_site_codes("10001")
    assert (
        len(site_codes) == 259 and
        site_codes[0] == 'ACAD1' and
        site_codes[-1] == 'ZION1'
    )
