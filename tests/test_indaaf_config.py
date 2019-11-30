import pytest
from obsdata import indaaf_config


@pytest.mark.parametrize('site_id,expect', (
    (1, 'Agoufou'),
    (2, 'Katibougou'),
))
def test_get_site_info(site_id, expect):
    site_info = indaaf_config.get_site_info(site_id)
    assert site_info.site == expect


def test_get_site_info_rasises():
    with pytest.raises(indaaf_config.InputError):
        indaaf_config.get_site_info(0)


@pytest.mark.parametrize('dataset,site_id,expect', (
    ('Precipitation', 1, 1),
    ('Gas', 1, 2),
    ('Aerosols', 1, 3),
    ('Meteo', 11, 10),
    ('Meteo', 12, 11),
    ('Meteo', 14, 12),
    ('Meteo', 13, 13),
))
def test_get_dataset_id(dataset, site_id, expect):
    assert indaaf_config.get_dataset_id(
        dataset, site_id) == expect


@pytest.mark.parametrize('dataset,site_id', (
    ('nodataset', 1),
    ('Meteo', 1),
))
def test_get_dataset_id_rasises(dataset, site_id):
    with pytest.raises(indaaf_config.InputError):
        indaaf_config.get_dataset_id(dataset, site_id)


def test_get_all_parameters():
    assert (
        indaaf_config.get_all_parameters("Meteo")
        == [
            "Wind speed", "Wind direction", "Temperature",
            "Relative humidity", "Rain"
        ]
    )


def test_get_all_site_codes():
    assert indaaf_config.get_all_site_codes() == range(1, 17)
