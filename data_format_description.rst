
Data format description
========================

Tables below describes a data file format specified in GAW Report_ no. 188
and this format is used here. The file format consists of a
header part and a data part and employs an ASCII encodeing.

.. _Report: https://webcache.googleusercontent.com/search?q=cache:nGfgmcgU2l4J:https://library.wmo.int/pmb_ged/wmo-td_1507.pdf+&cd=2&hl=sv&ct=clnk&gl=se&client=ubuntu


Header
-----------------


+-------+------------------------------+------------------------------------------------------+
|Line   |  Header item                 |   Content                                            |
+=======+==============================+======================================================+
|01     |  TITLE:                      |   Observation title                                  |
|       |                              |   (parameter, temporal representative, etc.)         |
+-------+------------------------------+------------------------------------------------------+
|02     |  FILE NAME:                  |   File name                                          |
+-------+------------------------------+------------------------------------------------------+
|03     |  DATA FORMAT:                |   Format version of this file that is given          |
|       |                              |   by the WDCGG                                       |
+-------+------------------------------+------------------------------------------------------+
|04     |  TOTAL LINES:                |   Number of total lines                              |
+-------+------------------------------+------------------------------------------------------+
|05     |  HEADER LINES:               |   Number of header lines                             |
+-------+------------------------------+------------------------------------------------------+
|06     |  DATA VERSION:               |   Data version of measurement data                   |
|       |                              |   (see Section 5.2). The version is given            |
|       |                              |   by the WDCGG, and managed using the date.          |
+-------+------------------------------+------------------------------------------------------+
|07     |  STATION NAME:               |   Name of the station where the data were            |
|       |                              |   observed                                           |
+-------+------------------------------+------------------------------------------------------+
|08     |  STATION CATEGORY:           |   GAW station category                               |
+-------+------------------------------+------------------------------------------------------+
|09     |  OBSERVATION CATEGORY:       |   Observation category defined in Section 3.3        |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|10     |  COUNTRY/TERRITORY:          |   The name of the country/territory where the        |
|       |                              |   station is located, or to which the ship or        |
|       |                              |   aircraft belongs is described here.                |
+-------+------------------------------+------------------------------------------------------+
|11     |  CONTRIBUTOR:                |   See section 2.2.1. (empty in meteorological        |
|       |                              |   data)                                              |
+-------+------------------------------+------------------------------------------------------+
|12     |  LATITUDE (degree):          |   Latitude of the station location (decimal)         |
+-------+------------------------------+------------------------------------------------------+
|13     |  LONGITUDE (degree):         |   Longitude of the station location (decimal)        |
+-------+------------------------------+------------------------------------------------------+
|14     |  ALTITUDE (m):               |   Altitude of the station above sea level            |
+-------+------------------------------+------------------------------------------------------+
|15     |  NUMBER OF SAMPLING HEIGHTS: |   The number of sampling heights from the            |
|       |                              |   ground for vertical profile observation.           |
|       |                              |   Unity for ground based observation.                |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|16     |  SAMPLING HEIGHTS (m):       |   The heights of the sampling intake from the        |
|       |                              |   ground. In the case of vertical profile            |
|       |                              |   observation, the heights are arranged in           |
|       |                              |   decreasing order                                   |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|17     |  CONTACT POINT:              |   E-mail address, fax number, or telephone           |
|       |                              |   number of Contact person for measurement           |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|18     |  PARAMETER:                  |   Observation parameter                              |
+-------+------------------------------+------------------------------------------------------+
|19     |  COVERING PERIOD:            |   Period of time in which measurement data           |
|       |                              |   are included.                                      |
+-------+------------------------------+------------------------------------------------------+
|20     |  TIME INTERVAL:              |   Temporal resolution of each measurement            |
|       |                              |   datum.                                             |
+-------+------------------------------+------------------------------------------------------+
|21     |  MEASUREMENT UNIT:           |   Unit of the mole fractions.                        |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|22     |  MEASUREMENT METHOD:         |   Measurement method employed.                       |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|23     |  SAMPLING TYPE:              |   See [Sampling type] in Annex 3.                    |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|24     |  TIME ZONE:                  |   Reported time zone with reference to UTC           |
+-------+------------------------------+------------------------------------------------------+
|25     |  REFERENCE SCALE:            |   Scale (traceability) employed in the               |
|       |                              |   measurement.                                       |
|       |                              |   (empty in meteorological data)                     |
+-------+------------------------------+------------------------------------------------------+
|26 - 29|  CREDIT FOR USE:             |   This is a formal notification for data users.      |
|       |                              |   "For scientific purposes, access to these data     |
|       |                              |   is unlimited and provided without charge. By their |
|       |                              |   use you accept that an offer of co-authorship      |
|       |                              |   will be made through personal contact with the     |
|       |                              |   data providers or owners whenever substantial      |
|       |                              |   use is made of their data. In all cases, an        |
|       |                              |   acknowledgement must be made to the data providers |
|       |                              |   or owners and the data centre when                 |
|       |                              |   these data areused within a publication.           |
+-------+------------------------------+------------------------------------------------------+
|30     |  COMMENTS:                   |   Any comments necessary for data usage are          |
|       |                              |   described.                                         |
|       |                              |   A definition of remarks (see Section 2.6           |
|       |                              |   and Table 8)                                       |
|       |                              |   is described if needed.                            |
+-------+------------------------------+------------------------------------------------------+


Records
----------------------------


+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|Item name  |  Number of | "No Data"       |  Content                       | Supplementary explanation              |
|           |  digits    |                 |                                |                                        |
+===========+============+=================+================================+========================================+
|DATE       |  10        | 9999-99-99      |  Beginning date of measurement | 7 digits are used only for ice core    |
|           |            |                 |  (YYYY-MM-DD)                  | to represent estimated year. The date  |
|           |            |                 |                                | for a monthly mean is the first date of|
|           |            |                 |                                | the month.                             |
|           |            |                 |                                | For example, 2005-02-01 is used        |
|           |            |                 |                                | for the monthly mean in February 2005. |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|TIME       |  5         | 99:99           |  Beginning time of measurement | The time for a monthly or daily mean   |
|           |            |                 |  (hh:mm)                       | is represented as 00:00.               |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|DATE       |  10        | 9999-99-99      |  End date of measurement       | In the case of a continuous            |
|           |            |                 |  (YYYY-MM-DD)                  | observation, end date is filled with   |
|           |            |                 |                                | ‘9999-99-99’.                          |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|TIME       |  5         | 99:99           |  End time of measurement       | In the case of a continuous            |
|           |            |                 |  (hh:mm)                       | observation, end time is filled with   |
|           |            |                 |                                | ‘99:99’.                               |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|DATA       |  10        | -99999.999      |  Mole fractions                | 16 digits are used only for VOCs       |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|ND         |  5         | -9999           |  Number of data used to        |                                        |
|           |            |                 |  average the data              |                                        |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|SD         |  7         | -999.99         |  Standard deviation            |                                        |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|F          |  5         | -9999           |  Data flag                     | The details of data flags should be    |
|           |            |                 |                                | specified by the Contributor in the    |
|           |            |                 |                                | metadata.                              |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|CS         |  2         | -9              |  Calculation Status indicating | This value is added by the WDCGG.      |
|           |            |                 |  who provides the data. “0”    |                                        |
|           |            |                 |  means the Contributor.        |                                        |
|           |            |                 |  “1” means the WDCGG.          |                                        |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+
|REM        |  9         | -99999999       |   Data remarks                 | Additional information on data to be   |
|           |            |                 |                                | included. The definition is described  |
|           |            |                 |                                | under “COMMENTS” of the header part.   |
+-----------+------------+-----------------+--------------------------------+----------------------------------------+


Example
--------------------------


C01 TITLE: OCf daily mean data

C02 FILE NAME: badl1.improve.as.cs.ocf.nl.da.dat

C03 DATA FORMAT: Version 1.0

C04 TOTAL LINES: 44

C05 HEADER LINES: 32

C06 DATA VERSION: 

C07 STATION NAME: Badlands NP

C08 STATION CATEGORY: global

C09 OBSERVATION CATEGORY: Air sampling observation at a stationary platform

C10 COUNTRY/TERRITORY: SD

C11 CONTRIBUTOR: improve

C12 LATITUDE: 43.74350

C13 LONGITUDE: -101.94120

C14 ALTITUDE: 736

C15 NUMBER OF SAMPLING HEIGHTS: 1

C16 SAMPLING HEIGHTS: 

C17 CONTACT POINT: nmhyslop@ucdavis.edu

C18 PARAMETER: OCf

C19 COVERING PERIOD: 2017-01-01 2017-01-31

C20 TIME INTERVAL: daily

C21 MEASUREMENT UNIT: ug/m^3 LC

C22 MEASUREMENT METHOD: 

C23 SAMPLING TYPE: continuous

C24 TIME ZONE: UTC

C25 MEASUREMENT SCALE: 

C26 CREDIT FOR USE: This is a formal notification for data users. 'For scientific purposes, access to these data is unlimited

C27 and provided without charge. By their use you accept that an offer of co-authorship will be made through personal contact

C28 with the data providers or owners whenever substantial use is made of their data. In all cases, an acknowledgement

C29 must be made to the data providers or owners and the data centre when these data are used within a publication.'

C30 COMMENT:

C31

C32   DATE  TIME       DATE  TIME       DATA    ND      SD     F CS       REM

2017-01-04 00:00 9999-99-99 99:99      0.398 -9999    0.09     8 -9 -99999999

2017-01-07 00:00 9999-99-99 99:99      0.495 -9999    0.09     8 -9 -99999999

2017-01-10 00:00 9999-99-99 99:99      0.658 -9999    0.10     8 -9 -99999999

2017-01-13 00:00 9999-99-99 99:99      0.851 -9999    0.11     8 -9 -99999999

2017-01-16 00:00 9999-99-99 99:99      0.483 -9999    0.09     8 -9 -99999999

2017-01-19 00:00 9999-99-99 99:99      0.779 -9999    0.10     8 -9 -99999999

2017-01-22 00:00 9999-99-99 99:99      0.431 -9999    0.09     8 -9 -99999999

2017-01-25 00:00 9999-99-99 99:99      0.175 -9999    0.08     8 -9 -99999999

2017-01-28 00:00 9999-99-99 99:99      0.213 -9999    0.08     8 -9 -99999999

2017-01-31 00:00 9999-99-99 99:99      0.210 -9999    0.08     8 -9 -99999999


File name convention 
--------------------------

The following file naming convention is used (inspired by the GAW Report no. 188):

**[Station code].[Contributor].[Observation category].[Sampling type].[Parameter].[Auxiliary item].[Data type].dat**

An example is:

*badl1.improve.as.cs.ocf.nl.da.dat*

[**Station code**]:

e.g. badl1 

[**Contributor**]:

e.g. improve

[**Observation category**]:

- as: Air observation at a stationary platform
- am: Air observation by a mobile platform
- ap: Vertical profile observation of air
- tc: Total column observation at a stationary platform
- hy: Hydrographic observation by ships
- ic: Ice core observation
- sf: Observation of surface seawater and overlying air

[**Sampling type**]:

- cn: Continuous or quasi-continuous in situ measurement
- fl: Analysis of air samples in flasks
- fi: Filter measurement
- rs: Remote sensing
- ic: Analysis of ice core samples
- bo: Analysis of samples in bottles
- ot: Other

[**Parameter**]:

e.g. ocf 

[**Auxiliary item**]:

If a data file is NOT identified uniquely with the codes above,
this field is filled with some characters to give a unique filename.
Most files have *nl* in this field, which means *NULL*.


[**Data type**]:

- ev: Event sampling data
- om: One-minute mean data
- tm: Ten-minute mean data
- hrxxxx: Hourly mean data observed in the year xxxx
- da: Daily mean data
- mo: Monthly mean data


Status flags
-------------------------------

The description of the various status flags are dot described in the header of the data file.
Table below describes status flages deployed by the *Federal Land Manager Environmental* Database_.

.. _Database: http://views.cira.colostate.edu/fed/QueryWizard/

+------------+------------------------------------------------------------------------------------+
|Status Flag | Description                                                                        |
+============+====================================================================================+
|H1 / 0      | Historical data that have not been assessed or validated.                          |
+------------+------------------------------------------------------------------------------------+
|I0 / 1      | Invalid value - unknown reason                                                     |
+------------+------------------------------------------------------------------------------------+
|I1 / 2      | Invalid value - known reason                                                       |
+------------+------------------------------------------------------------------------------------+
|I2 / 3      | Invalid value (-999), though sample-level flag seems valid (SEM)                   |
+------------+------------------------------------------------------------------------------------+
|M1 / 4      | Missing value because no value is available                                        |
+------------+------------------------------------------------------------------------------------+
|M2 / 5      | Missing value because invalidated by data originator                               |
+------------+------------------------------------------------------------------------------------+
|M3 / 6      | Missing value due to clogged filter                                                |
+------------+------------------------------------------------------------------------------------+
|NA / 7      | Not available from source data                                                     |
+------------+------------------------------------------------------------------------------------+
|V0 / 8      | Valid value                                                                        |
+------------+------------------------------------------------------------------------------------+
|V1 / 9      | Valid value but comprised wholly or partially of below detection limit data        |
+------------+------------------------------------------------------------------------------------+
|V2 / 10     | Valid estimated value                                                              |
+------------+------------------------------------------------------------------------------------+
|V3 / 11     | Valid interpolated value                                                           |
+------------+------------------------------------------------------------------------------------+
|V4 / 12     | Valid value despite failing to meet some QC or statistical criteria                |
+------------+------------------------------------------------------------------------------------+
|V5 / 13     | Valid value but qualified because of possible contamination                        |
+------------+------------------------------------------------------------------------------------+
|V6 / 14     | Valid value but qualified due to non-standard sampling conditions                  |
+------------+------------------------------------------------------------------------------------+
|V7 / 15     | Valid value set equal to the detection limit (DL) since the value was below the DL | 
+------------+------------------------------------------------------------------------------------+
|VM / 16     | Valid modeled value                                                                |
+------------+------------------------------------------------------------------------------------+
|VS / 17     | Valid substituted value                                                            |
+------------+------------------------------------------------------------------------------------+
