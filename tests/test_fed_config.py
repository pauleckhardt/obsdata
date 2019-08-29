import pytest


from obsdata.fed_config import (
    get_site_info,
    get_all_site_codes,
    get_parameter_info,
    validate_input,
    InputError
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
    assert site_info["SiteID"] == expect


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
        len(site_codes) == 259 and
        site_codes[0] == 'ACAD1' and
        site_codes[-1] == 'ZION1'
    )
