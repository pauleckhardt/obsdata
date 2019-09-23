==================
Observational-Data
==================

This is observational-data (obsdata), a Python package developed
in order to retrieve and store data from the
Federal Land Manager Environmental Database_
and The Acid Deposition Monitoring Network in East Asia (EANET_)
into a specific data format described in this document.

.. _Database: http://views.cira.colostate.edu/fed/QueryWizard/
.. _EANET: https://monitoring.eanet.asia/
	
Prerequisites
--------------------

The obsdata package has dependencies on a number of Python
packages:

  requests_: is an elegant and simple HTTP library for Python,

  bs4_: Beautiful Soup is a Python library for pulling data out of HTML and XML files.

  netcdf4_: a Python interface to the netCDF C library

  numpy_: the fundamental package for scientific computing with Python.

  pandas_: is a Python data analysis library, and can be used to rad Microsoft Excel files.

  xlrd_: Library for developers to extract data from Microsoft Excel spreadsheet files.

and these packages are available at PyPI_.

.. _requests: https://2.python-requests.org/en/master/
.. _bs4: https://pypi.org/project/beautifulsoup4/
.. _netcdf4: http://unidata.github.io/netcdf4-python/
.. _numpy: http://www.numpy.org/
.. _pandas: https://pandas.pydata.org/
.. _xlrd: https://pypi.org/project/xlrd/
.. _PyPI: https://pypi.org/

Installation
-------------------
	
Python packages should almost never be installed on the host
Python environment, in order to avoid problems that can arise
due to dependencies on different versions of packages.
The obsdata package is prefarbely installed
in a virtualenv_. A suitable virtualenv for the optimal-interpolation
package can be created by first installing the package
virtualenvwrapper_ on the host (so check that you are not
in a virutalenv before installing)
	
.. code-block:: bash
	
    sudo pip install virtualenvwrapper
	
Also add this to your shell startup file:
	
.. code-block:: bash
	
    export WORKON_HOME=$HOME/.virtualenvs  # The virtualenvs are stored here.
    export PROJECT_HOME=$HOME/Devel  # Location of your development project directories
    source /usr/local/bin/virtualenvwrapper.sh
	
Then you can create a virtualenv by:
	
.. code-block:: bash	
	
    mkvirtualenv --python=/usr/bin/python3.6 obsdata
	
and change to this envorinment by:
	
.. code-block:: bash
	  
    workon obsdata
	
and if yoy want to change back:
	
.. code-block:: bash
	
    deactivate

The obsdata package can be installed by:

.. code-block:: bash

    workon optimal-interpolation
    pip install -r requirements/requirements.txt
    python3 setup.py install

	
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/install.html
.. _virtualenv: https://virtualenv.pypa.io/en/latest/


Usage
------------------


Federal Land Manager Environmental Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The package contains two executable programs
for retrieving data from the
Federal Land Manager Environmental Database,
and the usage is described below:

.. code-block:: bash

  usage: get_fed_data  [-h] [-e DATA_FORMAT] [-q OUT_DIR]
                         dataset_id site-code parameter-code start-date end-date

  positional arguments:
    dataset_id            fed dataset id , e.g 10001 for 'IMPROVE Aerosol'
    site-code             fed site code, e.g BADL1 for 'Badlands NP'
    parameter-code        parameter code e.g. OCf
    start-date            start date, format YYYY-MM-DD
    end-date              end date, format YYYY-MM-DD

  optional arguments:
    -h, --help            show this help message and exit
    -e DATA_FORMAT, --data-format DATA_FORMAT
                          data format for saving file (dat or nc), default is dat
    -q OUT_DIR, --datadir-for-save OUT_DIR
                          data directory for saving output, default is /tmp


The program can for instance be invoked by:

.. code-block:: bash

    get_fed_data 10001 BADL1 OCf 2017-01-01 2017-01-31 -e dat -q /tmp

and then one month of OCf data from Badlands NP will be collected
and stored the /tmp directory (dataset-id, site-code, and parameter-code
are described in the following section).


The package also contains a script called get_all_fed_data.py,
which wraps around the get_fed_data.py script.
There is no user friendly interface to this script,
but the script can quite easily be modified
in order to retrieve desired data within a desired time period.
The code snippet found below is found within this script
and the meaning of the parameter should hopefully be understandable.
In this case the get_all_fed_data.py script retrieves
OCf data (from IMPROVE Aerosol dataset) at all sites and
between 2010-01-01 and 2015-12-31,
and creates a single file for each site.
The script also retrives O3 data (from the CASTNet Ozone - Hourly dataset),
and creates yearly files between 2010 and 2015 for all sites.


.. code-block:: python

    datasets_to_retrieve = [
        {
            "id": "10001",
            "parameter": "OCf",
            "start_date": datetime(2010, 1, 1),
            "end_date": datetime(2015, 12, 31),
            "timedelta_month": -1,
            "data_format": "dat",
            "out_dir": "/tmp",
        },
        {
            "id": "23005",
            "parameter": "O3",
            "start_date": datetime(2010, 1, 1),
            "end_date": datetime(2015, 12, 31),
            "timedelta_month": 12,
            "data_format": "dat",
            "out_dir": "/tmp",
        }
    ]


The obsdata package can also be used interactively

.. code-block:: python

    >>> from obsdata import fed_config

    # print available datasets (ids and names)
    >>>for dataset in fed_config.datasets:
    ...   print(dataset, fed_config.datasets[dataset].name)
    ... 
    54001 Air Sciences Speciated Aerosol
    20070 ARS Ozone - Hourly
    23007 CASTNET Dry Deposition - Annual
    23001 CASTNet Dry Chemistry - Weekly Filter Pack Concentrations
    23005 CASTNet Ozone - Hourly
    ....
    10001 IMPROVE Aerosol

    # get all site codes for a specific dataset
    >>>site_codes = fed_config.get_all_site_codes('10001')
    >>>site_codes 
    ['ACAD1', 'ADPI1', 'AGTI1', 'AMBL1', 'ARCH1', ... ]

    # get site information
    >>>site_info = fed_config.get_site_info('10001', 'ACAD1') 
    >>>site_info
    SiteInfo(id='1', code='ACAD1', name='Acadia NP', country='US', state='ME',
             latitude='44.38', longitude='-68.26', elevation='157')

    # get parameter information
    >>>parameters = fed_config.get_all_parameters('10001')
    >>>parameters
    [
        ParameterInfo(id='101', code='ALf'),
        ParameterInfo(id='136', code='NH4f'),
        ...
    ]


dataset-id, site-code, and parameter-code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data are retrieved by making requests to the Federal Land
Manager Environmental Database_.
Knowledge of a number of different ids are required
to make these requests, and these are described below.

Data from the Federal Land Manager Environmental Database
are organized in different datasets, e.g. the IMPROVE Aerosol dataset.
The obsdata package contains a csv file (data/datasets.csv),
that describes the id of 50 available datasets, and the first
rows of the file are shown below:

.. code-block:: bash

  ID;Name;Frequency
  54001;Air Sciences Speciated Aerosol;Daily
  20070;ARS Ozone - Hourly;Hourly
  23007;CASTNET Dry Deposition - Annual;Annual
  23001;CASTNet Dry Chemistry - Weekly Filter Pack Concentrations;Weekly
  23005;CASTNet Ozone - Hourly;Hourly
  23006;CASTNET Total Deposition By Pollutant - Annual;Annual
  23002;CASTNet Visibility Chemistry;Daily
  20009;EPA Carbon Monoxide (CO) - Hourly;Hourly
  20008;EPA Nitrogen Dioxide (NO2) - Hourly;Hourly
  20007;EPA Ozone - Hourly;Hourly
  20006;EPA PM10 Mass (81102) - Daily;Daily
  20005;EPA PM10 Mass (81102) - Hourly;Hourly
  20004;EPA PM2.5 Mass (88502) - Daily;Hourly
  20003;EPA PM2.5 Mass (88502) - Hourly;Hourly
  20001;EPA PM2.5 Mass FRM (88101) - Daily;Daily
  20011;EPA PM2.5 Mass FRM (88101) - Hourly;Hourly
  20002;EPA PM2.5 Speciation (CSN) - Daily;Daily
  20010;EPA Sulfur Dioxide (SO2) - Hourly;Hourly
  53001;Guelph Aerosol and Visibility Monitoring Program;Daily
  10001;IMPROVE Aerosol;Daily
  ...
  

A specific set of sites are associated to each dataset,
and the obsdata package contains a csv file for each
dataset (e.g data/fedsites_10001.csv
for the IMPROVE Aerosol dataset).
The fedsites_10001.csv contains information on
the 259 sites associated to the IMPROVE Aerosol dataset,
and the first rows of this file are shown below:

.. code-block:: bash

  SiteID,SiteCode,SiteName,CT,ST,EPACode,Lat,Lon,Elev,Start,End
  1,ACAD1,Acadia NP,US,ME,230090103,44.38,-68.26,157,03/02/88,11/28/18
  144,ADPI1,Addison Pinnacle,US,NY,361019000,42.09,-77.21,512,04/04/01,06/28/10
  100,AGTI1,Agua Tibia,US,CA,060659000,33.46,-116.97,508,12/20/00,11/28/18
  524,AMBL1,Ambler,US,AK,021889000,67.1,-157.86,78,09/03/03,11/29/04
  167,ARCH1,Arches NP,US,UT,490190101,38.78,-109.58,1722,03/02/88,12/29/99
  138,AREN1,Arendtsville,US,PA,420019000,39.92,-77.31,267,04/04/01,12/31/10
  25531,ATLA1,South Dekalb,US,GA,130890002,33.69,-84.29,243,03/01/04,11/28/18
  59,BADL1,Badlands NP,US,SD,460710001,43.74,-101.94,736,03/02/88,11/28/18
  ...
 
Each dataset is also associated to a specific set of parameters,
and the obsdata package contains a parameter csv file for each dataset
(e.g. parameters_10001.csv for the IMPROVE Aerosol dataset).
The parameters_10001.csv file contains ids for 115 parameters,
and the first rows of this file are shown below:

.. code-block:: bash

  Code,ID
  ALf,101
  ...
  EC1f,115
  EC2f,116
  EC3f,117
  ECf,114
  EC_UCD,3778
  OC1f,142
  OC2f,143
  OC3f,144
  OC4f,145
  OMCf,3016
  OPf,146
  OPTf,3699
  OCf,141
  ...

 


.. _ Database: http://views.cira.colostate.edu/fed/QueryWizard/


The Acid Deposition Monitoring Network in East Asia (EANET)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package contains an executable script for getting data from
EANET, and the usage is described below:

.. code-block:: bash

  usage: get_eanet_data    [-h] [-e DATA_FORMAT] [-q OUT_DIR] [-x XLS_DIR]
                           dataset_id site-code parameter-code start-date
                           end-date

  positional arguments:
    dataset_id            dataset_id: 1 for 'Dry Monthly'
    site-code             eanet site code, e.g JPA001 for 'Rishiri', use 'all'
                          for getting data from all available sites
    parameter-code        parameter code e.g. SO2, use 'all' for getting data
                          from all available parameters
    start-date            start date, format YYYY-MM-DD
    end-date              end date, format YYYY-MM-DD
 
  optional arguments:
    -h, --help            show this help message and exit
    -e DATA_FORMAT, --data-format DATA_FORMAT
                          data format for saving file (nc or dat), default is
                          dat
    -q OUT_DIR, --datadir-for-save OUT_DIR
                          data directory for saving output, default is /tmp
    -x XLS_DIR, --datadir-for-xls XLS_DIR
                          data directory for saving eanet xls files, default is
                          /tmp


and the script can e.g. be invoked by:
 
.. code-block:: bash

   get_eanet_data 1 JPA001 SO2 2001-01-01 2017-12-31 -e dat -q /tmp -x /tmp

So far only the 'Dry Monthly' dataset is handled, but this will be extended.
The script downloads an Excel file for each year (this file is common for
all parameters within the dataset), and the -x parameter determines
where these files are stored.
If the file already exists in the data directory (from a previous
run of the program) the file is not downloaded
again, and hence the exceution of the script is much faster.
Data found within the Excel files are then merged into a data
format described in the following section.

The data directory of the package contains a file
named 'eanet_sites.txt' that contains data about the location
of the sites. This information is not provided in the
Excel sheets, and information from the eanet_sites.txt 
are used to produce the output data.


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
- an: Annual mean data

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
