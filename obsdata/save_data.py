import os
from netCDF4 import Dataset, date2num


class NotImplementedError(Exception):
    pass


def get_output_filename(data, extension):
    '''returns a filename conating the follwing parts

       [Station code].[Contributor].[Observation category].
       [Sampling type].[Parameter].[Auxiliary item].[Data type].

       ex: ryo239n00.jma.as.cn.cfc113.nl.hr2007.dat

       [Observation category]
         as: Air observation at a stationary platform
         am: Air observation by a mobile platform
         ap: Vertical profile observation of air
         tc: Total column observation at a stationary platform
         hy: Hydrographic observation by ships
         ic: Ice core observation
         sf: Observation of surface seawater and overlying air

       [Sampling type]
         cn: Continuous or quasi-continuous in situ measurement
         fl: Analysis of air samples in flasks
         fi: Filter measurement
         rs: Remote sensing
         ic: Analysis of ice core samples
         bo: Analysis of samples in bottles
         ot Other

       [Data type]
         ev: Event sampling data
         om: One-minute mean data
         tm: Ten-minute mean data
         hrxxxx: Hourly mean data observed in the year xxxx
         da: Daily mean data
         mo: Monthly mean data

       [Auxiliary item]
         If a data file is NOT identified uniquely with the codes above,
         this field is filled with some characters to give a unique
         filename.
         nl: Null
    '''
    if data.observation_category == (
            "Air sampling observation at a stationary platform"):
        observation_category = "as"
    else:
        raise(NotImplementedError)

    if data.sampling_type == "continuous":
        sampling_type = "cs"
    else:
        raise(NotImplementedError)

    if data.time_interval == "daily":
        data_type = "da"
    elif data.time_interval == "hourly":
        data_type = "hr{}".format(data.records[0].datetime.year)
    else:
        raise(NotImplementedError)

    return "{0}.{1}.{2}.{3}.{4}.{5}.{6}.{7}".format(
        data.station_code.lower(),
        data.contributor,
        observation_category,
        sampling_type,
        data.parameter_code.lower(),
        "nl",
        data_type,
        extension
    )


def save_data_txt(out_dir, data):
    """
        the 'World Data Centre' format is used,
        It has 32 header lines which describes the site and data,
        then the data-records.
        see document data_format_description.rst
        for more information
    """

    nr_digits_date = 10
    nr_digits_time = 5
    nr_digits_data = 10
    nr_digits_nd = 5
    nr_digits_sd = 7
    nr_digits_f = 5
    nr_digits_cs = 2
    nr_digits_rem = 9

    header_lines = 32

    title = "{0} {1} mean data".format(
        data.parameter_code, data.time_interval)

    file_name = get_output_filename(data, "dat")

    covering_period = "{0} {1}".format(
        data.records[0].datetime.strftime("%Y-%m-%d"),
        data.records[-1].datetime.strftime("%Y-%m-%d")
    )

    file_header_rows = [
        "C01 TITLE: {}".format(title),
        "C02 FILE NAME: {}".format(file_name),
        "C03 DATA FORMAT: {}".format("Version 1.0"),
        "C04 TOTAL LINES: {}".format(header_lines + len(data.records)),
        "C05 HEADER LINES: {}".format(header_lines),
        "C06 DATA VERSION: {}".format(data.data_version),
        "C07 STATION NAME: {}".format(data.station_name),
        "C08 STATION CATEGORY: {}".format(data.station_category),
        "C09 OBSERVATION CATEGORY: {}".format(data.observation_category),
        "C10 COUNTRY/TERRITORY: {}".format(data.country_territory),
        "C11 CONTRIBUTOR: {}".format(data.contributor),
        "C12 LATITUDE: {}".format(data.latitude),
        "C13 LONGITUDE: {}".format(data.longitude),
        "C14 ALTITUDE: {}".format(data.altitude),
        "C15 NUMBER OF SAMPLING HEIGHTS: {}".format(
            data.nr_of_sampling_heights),
        "C16 SAMPLING HEIGHTS: {}".format(data.sampling_heights),
        "C17 CONTACT POINT: {}".format(data.contact_point),
        "C18 PARAMETER: {}".format(data.parameter_code),
        "C19 COVERING PERIOD: {}".format(covering_period),
        "C20 TIME INTERVAL: {}".format(data.time_interval),
        "C21 MEASUREMENT UNIT: {}".format(data.measurement_unit),
        "C22 MEASUREMENT METHOD: {}".format(data.measurement_method),
        "C23 SAMPLING TYPE: {}".format(data.sampling_type),
        "C24 TIME ZONE: {}".format(data.time_zone),
        "C25 MEASUREMENT SCALE: {}".format(data.measurement_scale),
        "C26 CREDIT FOR USE: This is a formal notification for data users. 'For scientific purposes, access to these data is unlimited",  # noqa
        "C27 and provided without charge. By their use you accept that an offer of co-authorship will be made through personal contact",  # noqa
        "C28 with the data providers or owners whenever substantial use is made of their data. In all cases, an acknowledgement",  # noqa
        "C29 must be made to the data providers or owners and the data centre when these data are used within a publication.'",  # noqa
        "C30 COMMENT:",
        "C31",
        "C32 {0} {1} {2} {3} {4} {5} {6} {7} {8} {9}".format(
            "DATE".rjust(nr_digits_date - 4),
            "TIME".rjust(nr_digits_time),
            "DATE".rjust(nr_digits_date),
            "TIME".rjust(nr_digits_time),
            "DATA".rjust(nr_digits_data),
            "ND".rjust(nr_digits_nd),
            "SD".rjust(nr_digits_sd),
            "F".rjust(nr_digits_f),
            "CS".rjust(nr_digits_cs),
            "REM".rjust(nr_digits_rem)
        )
    ]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, file_name), mode='wb') as outfile:
        for row in file_header_rows:
            print(row)
            outfile.write("{}\n".format(row).encode("ascii"))

        for record in data.records:

            value = record.value if not record.value == -999 else -99999.999
            unc = (
                record.uncertainty if not record.uncertainty == -999
                else -999.99
            )
            status_flag = record.status if not record.status == -999 else -9999
            nr_of_samples = (
                record.nr_of_samples if not record.nr_of_samples == -999
                else -9999
            )

            outfile.write(
                "{0} 9999-99-99 99:99 {1} {2} {3} {4} {5} {6}\n".format(
                    record.datetime.strftime("%Y-%m-%d %H:%M"),
                    "{:10.3f}".format(value),
                    "{:5}".format(nr_of_samples),
                    "{:7.2f}".format(unc),
                    "{:5}".format(status_flag),
                    "-9",
                    "-99999999",
                ).encode("ascii")
            )


def save_data_netcdf(out_dir, data):

    # TODO: fix format (talk to dave)

    file_name = get_output_filename(data, "nc")

    output_file = os.path.join(out_dir, file_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    dataset = Dataset(output_file, "w", format="NETCDF4")

    # global attributes

    dataset.station_name = data.station_name
    dataset.latitude = float(data.latitude)
    dataset.longitude = float(data.longitude)
    dataset.altitude = float(data.altitude)

    # dimensions

    timedim = dataset.createDimension("time", len(data.records))
    chardim = dataset.createDimension('nchar', 2)

    # time

    time = dataset.createVariable("time", "f8", (timedim.name,))
    time.standard_name = "time"
    time.long_name = "time of measurement"
    time.units = "days since 1900-01-01 00:00:00 UTC"
    time.calendar = "gregorian"
    time[:] = [
        date2num(record.datetime, time.units, calendar=time.calendar)
        for record in data.records
    ]

    parameter = dataset.createVariable(
        data.parameter_code, "f8", (timedim.name,), fill_value=-9999.)
    parameter.standard_name = data.parameter
    parameter.missing_value = -9999.
    parameter.units = data.measurement_unit
    parameter[:] = [record.value for record in data.records]

    # uncertainty

    parameter = dataset.createVariable(
        "Unc", "f8", (timedim.name,), fill_value=-9999.)
    parameter.standard_name = "Uncertainty"
    parameter.missing_value = -9999.
    parameter.units = data.measurement_unit
    parameter[:] = [record.uncertainty for record in data.records]

    # status flag

    parameter = dataset.createVariable(
        "SF", "c", (timedim.name, chardim.name))
    parameter.standard_name = "StatusFlag"
    description = ""
    for index in range(len(data.status_flags['Status Flag'])):
        description += "{0}: {1};".format(
            data.status_flags["Status Flag"][index],
            data.status_flags["Description"][index],
        )
    parameter[:] = [record.status_flag for record in data.records]

    dataset.close()
