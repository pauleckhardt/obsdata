import pytest
import os
import datetime
from obsdata import indaaf_data, indaaf_config, save_data


indaaf_file = os.path.join(
    os.path.dirname(__file__), "Gas-1-O3.csv"
)


@pytest.fixture
def o3_data():
    dataset = "Gas"
    parameter = "O3"
    site_code = 1
    site_info = indaaf_config.get_site_info(site_code)
    dataset_info = indaaf_config.DATASETS[
        [row["name"] for row in indaaf_config.DATASETS].index(
            dataset)
    ]
    parameter_info = indaaf_config.get_parameter_id(
        parameter, dataset)
    return indaaf_data.get_records(
        indaaf_file,
        parameter,
        site_info,
        parameter_info,
        dataset_info
    )


@pytest.mark.parametrize('parameter,expect', (
    ('data_version', '?'),
    ('station_name', 'Agoufou'),
    ('station_code', '1'),
    ('station_category', 'global'),
    (
        'observation_category',
        'Air sampling observation at a stationary platform'
    ),
    ('country_territory', 'Mali'),
    ('contributor', 'indaaf'),
    ('latitude', 15.15),
    ('longitude', 0.6667),
    ('altitude', 300.0),
    ('nr_of_sampling_heights', 1),
    ('sampling_heights', '?'),
    (
        'contact_point',
        'corinne.galy-lacaux@aero.obs-mip.fr'
    ),
    ('dataset', 'Gas'),
    ('parameter', 'O3'),
    ('parameter_code', 'O3'),
    ('time_interval', 'monthly'),
    ('measurement_unit', 'ppb'),
    ('measurement_method', '?'),
    ('sampling_type', 'continuous'),
    ('time_zone', 'UTC'),
    ('measurement_scale', '?'),
    ('status_flags', '?'),
))
def test_get_records_correct_info(o3_data, parameter, expect):
    assert getattr(o3_data, parameter) == expect


def test_get_records(o3_data):
    assert o3_data.records[0] == save_data.Record(
        start_datetime=datetime.datetime(2005, 1, 1, 0, 0),
        end_datetime=-9999,
        value=7.26,
        uncertainty=-999,
        status=-999,
        status_flag=-999,
        nr_of_samples=-999
    )
    assert o3_data.records[-1] == save_data.Record(
        start_datetime=datetime.datetime(2011, 9, 1, 0, 0),
        end_datetime=-9999,
        value=18.42,
        uncertainty=-999,
        status=-999,
        status_flag=-999,
        nr_of_samples=-999
    )
