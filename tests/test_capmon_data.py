import os
import pytest
import pandas as pd
import datetime
from obsdata import capmon_data, capmon_config, save_data


capmon_file = os.path.join(
    os.path.dirname(__file__),
    "AtmosphericPrecipitationChemistry-MajorIons-CAPMoN-AllSites-1989.csv"  # noqa
)


@pytest.fixture
def capmon_file_rows():
    with open(capmon_file, "rb") as the_file:
        return the_file.readlines()


@pytest.mark.parametrize('table_name,expect', (
    ('Data validity flags', 32),
    ('Site information', 49),
    ('CAPMoN_Precip_Chemistry', 91),
))
def test_get_table_row_start(
        capmon_file_rows, table_name, expect):
    row_start = capmon_data.get_table_row_start(
        table_name, capmon_file_rows)
    assert row_start == expect


@pytest.mark.parametrize('table_name,expect', (
    ('Data validity flags', (40, 47)),
    ('Site information', (59, 89)),
    ('CAPMoN_Precip_Chemistry', (116, 10058)),
))
def test_get_table_rows_data(
        capmon_file_rows, table_name, expect):
    row_start = capmon_data.get_table_row_start(
        table_name, capmon_file_rows)
    table_rows = capmon_data.get_table_rows_data(
        capmon_file_rows, row_start)
    assert table_rows == expect


@pytest.mark.parametrize('row_start,row_end,id,expect', (
    (
        32, 47, b"TABLE COLUMN NAME--SHORT FORM", [
            'DataValidityFlag',
            'DataValidityFlagDescription',
            'DataValidityFlagEnhDesc'
        ]
    ),
    (
        91, 10058, b"TABLE COLUMN NAME--CHEMICAL FORMULA", [
            '', '', '', '', '', '', '', '', '', '', '',
            'pH', 'pH', 'H+', 'H+', 'SO42-', 'SO42-', 'SO42-',
            'nss-SO42-', 'nss-SO42-', 'nss-SO42-',
            'NO3-', 'NO3-', 'NO3-', 'Cl-', 'Cl-', 'Cl-',
            'NH4+', 'NH4+', 'NH4+', 'Na+', 'Na+', 'Na+',
            'Ca2+', 'Ca2+', 'Ca2+', 'Mg2+', 'Mg2+', 'Mg2+',
            'K+', 'K+', 'K+', '', '', '', '', '', '', '',
            '', '', '', '', '', ''
        ]
    ),
))
def test_get_data_from_row(
        capmon_file_rows, row_start, row_end, id, expect):
    data = capmon_data.get_data_from_row(
        capmon_file_rows, row_start, row_end, id)
    print(data)
    assert data == expect


@pytest.mark.parametrize('parameter,expect', (
    ('pH', 'pH'),
    ('H+', 'H_mgL'),
    ('SO42-', 'SO4_mgL'),
    ('nss-SO42-', 'SO4nonseasalt_mgL'),
    ('NO3-', 'NO3_mgL'),
    ('Cl-', 'Cl_mgL'),
    ('NH4+', 'NH4_mgL'),
    ('Na+', 'Na_mgL'),
    ('Ca2+', 'Ca_mgL'),
    ('Mg2+', 'Mg_mgL'),
    ('K+', 'K_mgL'),
))
def test_get_header(parameter, expect):
    header = capmon_data.get_header(
        capmon_file, 'CAPMoN_Precip_Chemistry', parameter
    )
    assert header == expect


@pytest.mark.parametrize('parameter,expect', (
    ('pH', 'pH unit'),
    ('H+', 'mg/L (milligram per liter)'),
    ('SO42-', 'mg/L (milligram per liter)'),
    ('nss-SO42-', 'mg/L (milligram per liter)'),
    ('NO3-', 'mg/L (milligram per liter)'),
    ('Cl-', 'mg/L (milligram per liter)'),
    ('NH4+', 'mg/L (milligram per liter)'),
    ('Na+', 'mg/L (milligram per liter)'),
    ('Ca2+', 'mg/L (milligram per liter)'),
    ('Mg2+', 'mg/L (milligram per liter)'),
    ('K+', 'mg/L (milligram per liter)'),
))
def test_get_units(parameter, expect):
    header = capmon_data.get_units(
        capmon_file, 'CAPMoN_Precip_Chemistry', parameter
    )
    assert header == expect


def test_get_data_from_csvfile():
    data = capmon_data.get_data_from_csvfile(
        capmon_file, 'Data validity flags')
    assert isinstance(data, pd.DataFrame)
    assert set(data.columns) == set([
       'DataValidityFlag',
       'DataValidityFlagDescription',
       'DataValidityFlagEnhDesc'
    ])
    assert set(
        data["DataValidityFlag"].values
    ) == set(["V0", "V1", "V2", "V7", "M1", "M2"])
    assert set(
        data['DataValidityFlagDescription'].values
    ) == set([
        'Valid value',
        'Valid value - below detection limit',
        'Valid value - extreme or unusual value assessed and considered valid',  # noqa
        'Valid value - below detection limit and reported as the detection limit or lowest measureable value',  # noqa
        'Missing value - no value available',
        'Missing value - invalidated by Principal Investigator',
    ])


def test_get_records():
    dataset = "CAPMoN_Precip_Chemistry"
    site_code = "CAPMCAAB1EST"
    data = capmon_data.get_data_from_csvfile(
        capmon_file, dataset)
    data = data.loc[data.SiteID == site_code]
    site_info = capmon_config.validate_site_id(
        dataset, site_code)
    target_parameter = "H_mgL"
    status_parameter = "H_mgL_Flag"
    units = "mg/L (milligram per liter)"
    parameter = "H+"
    time_interval = "daily"
    obsdata_records = capmon_data.get_records(
        data,
        site_info,
        target_parameter,
        status_parameter,
        units,
        dataset,
        parameter,
        time_interval
    )
    assert len(obsdata_records.records) == 358
    assert (
        obsdata_records.records[0] ==
        save_data.Record(
            start_datetime=datetime.datetime(1989, 1, 1, 17, 0),
            end_datetime=datetime.datetime(1989, 1, 2, 16, 0),
            value=-999.0,
            uncertainty=-999,
            status=4,
            status_flag='M1',
            nr_of_samples=-999
        )
    )
    assert (
        obsdata_records.records[13] ==
        save_data.Record(
            start_datetime=datetime.datetime(1989, 1, 14, 16, 0),
            end_datetime=datetime.datetime(1989, 1, 15, 17, 0),
            value=0.012023, uncertainty=-999,
            status=0,
            status_flag='V0',
            nr_of_samples=-999
        )
    )


def test_merge_data_many_years():
    dataset = "CAPMoN_Precip_Chemistry"
    parameter = "H+"
    site_code = "CAPMCAAB1EST"
    site_info = capmon_config.validate_site_id(
        dataset, site_code)
    data = capmon_data.merge_data_many_years(
        dataset,
        parameter,
        site_info,
        1989,
        1989,
        os.path.dirname(__file__)
    )
    assert len(data.records) == 358
    assert (
        data.records[0] ==
        save_data.Record(
            start_datetime=datetime.datetime(1989, 1, 1, 17, 0),
            end_datetime=datetime.datetime(1989, 1, 2, 16, 0),
            value=-999.0,
            uncertainty=-999,
            status=4,
            status_flag='M1',
            nr_of_samples=-999
        )
    )
    assert (
        data.records[13] ==
        save_data.Record(
            start_datetime=datetime.datetime(1989, 1, 14, 16, 0),
            end_datetime=datetime.datetime(1989, 1, 15, 17, 0),
            value=0.012023, uncertainty=-999,
            status=0,
            status_flag='V0',
            nr_of_samples=-999
        )
    )
    assert data.data_version == '?'
    assert data.station_name == 'Esther'
    assert data.station_code == 'CAPMCAAB1EST'
    assert data.station_category == 'global'
    assert data.observation_category == (
        'Air sampling observation at a stationary platform')
    assert data.country_territory == 'CA (CANADA)'
    assert data.contributor == 'capmon'
    assert data.latitude == pytest.approx(51.6697, abs=1e-4)
    assert data.longitude == pytest.approx(-110.2065, abs=1e-4)
    assert data.altitude == 702
    assert data.nr_of_sampling_heights == 1
    assert data.sampling_heights == '?'
    assert data.contact_point == 'enviroinfo@canada.ca'
    assert data.dataset == 'CAPMoN_Precip_Chemistry'
    assert data.parameter == 'H+'
    assert data.parameter_code == 'H+'
    assert data.time_interval == 'daily'
    assert data.measurement_unit == 'mg/L (milligram per liter)'
    assert data.measurement_method == '?'
    assert data.sampling_type == 'continuous'
    assert data.time_zone == 'UTC'
    assert data.measurement_scale == '?'
    assert data.status_flags == '?'
