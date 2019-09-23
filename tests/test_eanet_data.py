import pytest
import os
from datetime import datetime
import pandas as pd
from obsdata.eanet_data import EanetSheetExtractor


@pytest.fixture
def sheet():
    xlsfile = os.path.join(
        os.path.dirname(__file__),
        "Dry2005Monthly.xls"
    )
    return pd.read_excel(xlsfile, sheet_name='O3')


def test_sheet_extractor_year(sheet):
    record_extractor = EanetSheetExtractor(sheet)
    assert record_extractor.get_year() == 2005


def test_sheet_extractor_unit(sheet):
    record_extractor = EanetSheetExtractor(sheet)
    assert record_extractor.get_unit() == 'ppb'


@pytest.mark.parametrize('parameter,expect', (
    ('Site', 'Site'),
    ('Country', 'Country'),
))
def test_sheet_extractor_locate_variable(sheet, parameter, expect):
    record_extractor = EanetSheetExtractor(sheet)
    row, column = record_extractor.locate_variable(parameter)
    assert record_extractor.sheet.loc[row][column] == expect


def test_sheet_extractor_get_all_sites(sheet):
    record_extractor = EanetSheetExtractor(sheet)
    sites = record_extractor.get_sites()
    assert len(sites) == 17


@pytest.mark.parametrize('index,expect', (
    (0, {"site": "Rishiri", "row_start": 3, "row_end": 6, "column": 1}),
    (16, {"site": "Chiang Mai", "row_start": 67, "row_end": 70, "column": 1}),
))
def test_sheet_extractor_get_sites(sheet, index, expect):
    record_extractor = EanetSheetExtractor(sheet)
    sites = record_extractor.get_sites()
    assert sites[index] == expect


@pytest.mark.parametrize('index, parameter, expect', (
    (0, "datetime", datetime(2005, 1, 1)),
    (0, "value", 42.5027),
    (0, "uncertainty", 7.6041),
    (11, "datetime", datetime(2005, 12, 1)),
    (11, "value", 40.2384),
    (11, "uncertainty",  5.8258),

))
def test_sheet_extractor_get_records(sheet, index, parameter, expect):
    record_extractor = EanetSheetExtractor(sheet)
    site = {"site": "Rishiri", "row_start": 3, "row_end": 6, "column": 1}
    _, records = record_extractor.get_records(site)
    assert len(records) == 12
    if parameter == "datetime":
        assert getattr(records[index], parameter) == expect
    else:
        assert getattr(records[index], parameter) == pytest.approx(
            expect, rel=1e-5)
