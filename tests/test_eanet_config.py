import pytest
from obsdata import eanet_config


@pytest.mark.parametrize('lat,lon,expect', (
    ('11°30\'45"N', '104°30\'36"E', (11.5125, 104.51)),
    ('11°30\'45"S', '104°30\'36"E', (-11.5125, 104.51)),
    ('11°30\'45"N', '104°30\'36"W', (11.5125, -104.51)),
    ('11°30\'45"S', '104°30\'36"W', (-11.5125, -104.51)),
))
def test_coordinates_to_decimal_form(lat, lon, expect):
    lat_dec, lon_dec = eanet_config.coordinates_to_decimal_form(
        lat, lon)
    assert lat_dec == expect[0] and lon_dec == expect[1]


def test_get_all_site_codes():
    site_codes = eanet_config.get_all_site_codes()
    assert len(site_codes) == 64
    assert site_codes[0] == 'KHA001'
    assert site_codes[-1] == 'VNA007'


@pytest.mark.parametrize('site_code,expect', (
    ('KHA001', 'Phnom Penh'),
    ('VNA007', 'Yen Bai'),
))
def test_get_site_info(site_code, expect):
    site_info = eanet_config.get_site_info(site_code)
    assert site_info.site == expect


def test_get_site_info_raises():
    with pytest.raises(eanet_config.InputError):
        eanet_config.get_site_info("nosite")


def test_validate_input():
    assert eanet_config.validate_input(
        1, 'KHA001', 'Ca2+')


def test_validate_input_raises():
    with pytest.raises(eanet_config.InputError):
        eanet_config.validate_input(1, 'KHA001', 'undef')
