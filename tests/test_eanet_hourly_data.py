import pytest
import os
from datetime import datetime
from obsdata.eanet_hourly_data import (
    EanetWetDataExtractor, EanetDryDataExtractor,
)


wet_deposition_file = os.path.join(
    os.path.dirname(__file__),
    "CNA004_2006_wet_deposition.csv"
)


dry_deposition_file = os.path.join(
    os.path.dirname(__file__),
    "IDA001_2007_dry_deposition_passive_sampler.csv"
)


def test_dry_data_extractor_get_products():
    data_extractor = EanetDryDataExtractor(dry_deposition_file, "O3")
    assert not data_extractor.parameter_in_dataset()
    assert set(data_extractor.get_products()) == set(["SO2", "NO2"])


@pytest.mark.parametrize('target, index, parameter, expect', (
    ("SO2", 0, "start_datetime", datetime(2006, 12, 31, 0, 0)),
    ("SO2", 0, "end_datetime", datetime(2007, 1, 5, 0, 0)),
    ("SO2", 0, "value", 3.0),
    ("SO2", 60, "start_datetime", datetime(2007, 12, 25, 0, 0)),
    ("SO2", 60, "end_datetime", datetime(2007, 12, 30, 0, 0)),
    ("SO2", 60, "value", 20.6),
    ("NO2", 0, "start_datetime", datetime(2006, 12, 31, 0, 0)),
    ("NO2", 0, "end_datetime", datetime(2007, 1, 5, 0, 0)),
    ("NO2", 0, "value", 1.2),
    ("NO2", 60, "start_datetime", datetime(2007, 12, 25, 0, 0)),
    ("NO2", 60, "end_datetime", datetime(2007, 12, 30, 0, 0)),
    ("NO2", 60, "value", 2.8),
))
def test_dry_data_extractor_get_records(target, index, parameter, expect):
    data_extractor = EanetDryDataExtractor(dry_deposition_file, target)
    records = data_extractor.get_records()
    if parameter in ["start_datetime", "end_datetime"]:
        assert getattr(records[index], parameter) == expect
    else:
        assert getattr(records[index], parameter) == pytest.approx(
            expect, rel=1e-5)


def test_wet_data_extractor_get_products():
    data_extractor = EanetWetDataExtractor(wet_deposition_file, "H2O")
    assert not data_extractor.parameter_in_dataset()
    products = data_extractor.get_products()
    assert set([
        'SO42-', 'NO3-', 'Cl-', 'F-', 'NH4+', 'Na+',
        'K+', 'Ca2+', 'Mg2+', 'EC', 'pH'
    ]).issubset(products)


@pytest.mark.parametrize('target, index, parameter, expect', (
    ("SO42-", 2, "start_datetime", datetime(2006, 1, 3, 9, 0)),
    ("SO42-", 2, "end_datetime", datetime(2006, 1, 4, 9, 0)),
    ("SO42-", 2, "value", 1097.8),
    ("SO42-", 361, "start_datetime", datetime(2006, 12, 28, 9, 0)),
    ("SO42-", 361, "end_datetime", datetime(2006, 12, 29, 9, 0)),
    ("SO42-", 361, "value", 870.9),
    ("NO3-", 2, "start_datetime", datetime(2006, 1, 3, 9, 0)),
    ("NO3-", 2, "end_datetime", datetime(2006, 1, 4, 9, 0)),
    ("NO3-", 2, "value", 553.3),
    ("NO3-", 361, "start_datetime", datetime(2006, 12, 28, 9, 0)),
    ("NO3-", 361, "end_datetime", datetime(2006, 12, 29, 9, 0)),
    ("NO3-", 361, "value", 243.7),
))
def test_wet_data_extractor_get_records(target, index, parameter, expect):
    data_extractor = EanetWetDataExtractor(wet_deposition_file, target)
    records = data_extractor.get_records()
    if parameter in ["start_datetime", "end_datetime"]:
        assert getattr(records[index], parameter) == expect
    else:
        assert getattr(records[index], parameter) == pytest.approx(
            expect, rel=1e-5)
