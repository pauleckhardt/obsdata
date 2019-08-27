
Data format description
========================

Tables below describes a data file format specified in GAW Report_ no 188
and this format is used here.

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
