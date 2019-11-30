import pytest
from obsdata import capmon_config


def test_validate_dataset_raises():
    with pytest.raises(capmon_config.InputError):
        capmon_config.validate_dataset("nodataset")


def test_validate_dataset():
    assert capmon_config.validate_dataset(
        "CAPMoN_Ozone")


def test_get_site_info():
    site_info = capmon_config.get_site_info(
        "CAPMoN_Precip_Chemistry", "CAPMCAAB1EST")
    assert site_info.code == "CAPMCAAB1EST"


def test_get_site_info_raises():
    with pytest.raises(capmon_config.InputError):
        capmon_config.get_site_info(
            "CAPMoN_Precip_Chemistry", "nosite")


def test_validate_parameter():
    assert capmon_config.validate_parameter("CAPMoN_Ozone",  "O3")


def test_validate_parameter_raises():
    with pytest.raises(capmon_config.InputError):
        capmon_config.validate_parameter("CAPMoN_Ozone",  "O4")
