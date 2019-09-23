import pytest


from obsdata.eanet_config import (
    coordinates_to_decimal_form,
    get_site_information
)


@pytest.mark.parametrize('lat,lon,expect', (
    ('11°30\'45"N', '104°30\'36"E', (11.5125, 104.51)),
    ('11°30\'45"S', '104°30\'36"E', (-11.5125, 104.51)),
    ('11°30\'45"N', '104°30\'36"W', (11.5125, -104.51)),
    ('11°30\'45"S', '104°30\'36"W', (-11.5125, -104.51)),
))
def test_coordinates_to_decimal_form(lat, lon, expect):
    lat_dec, lon_dec = coordinates_to_decimal_form(lat, lon)
    assert lat_dec == expect[0] and lon_dec == expect[1]


@pytest.mark.parametrize('index,parameter,expect', (
    (0, "country", "Cambodia"),
    (0, "site", "Phnom Penh"),
    (0, "code", "KHA001"),
    (0, "classification", "Urban"),
    (0, "latitude",  11.555),
    (0, "longitude", 104.93889),
    (0, "altitude", "12"),
    (-1, "country", "Vietnam"),
    (-1, "site", "Yen Bai"),
    (-1, "code", "VNA007"),
    (-1, "classification", "Rural"),
    (-1, "latitude", 21.70778),
    (-1, "longitude",  104.87472),
    (-1, "altitude", "56"),
))
def test_get_site_info(index, parameter, expect):
    sites = get_site_information()
    assert getattr(sites[index], parameter) == expect
