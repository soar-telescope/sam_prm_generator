#!/usr/bin/env python 
# -*- coding: utf8 -*-

from __future__ import division, print_function

import argparse
import datetime

from astropy.coordinates import SkyCoord
from astropy import units as u

__author__ = 'Bruno Quint'

argument_parser = argparse.ArgumentParser(
    description="Script that reads a list of targets and returns a PRM file to "
                "be submitted to the SpaceTrack website for runs with SAM.")

argument_parser.add_argument('targets_filename', type=str, nargs=1,
                             help="Name of the file that contains list of "
                                  "targets that will be observed")

argument_parser.add_argument('year', type=int, nargs=1,
                             help="Year of the beginning of the observing "
                                  "night.")

argument_parser.add_argument('month', type=int, nargs=1,
                             help="Month of the beginning of the observing "
                                  "night")

argument_parser.add_argument('day', type=int, nargs=1,
                             help="Day of the beginning of the observing night")

argument_parser.add_argument('utstart', type=str, nargs=1,
                             help="UT hour that the observation starts. "
                                  "[hh:mm:ss]")

argument_parser.add_argument('utend', type=str, nargs=1,
                             help="UT hour that the observation stops "
                                  "[hh:mm:ss]")

args = argument_parser.parse_args()

# PRM File Template ==========================================================
template = \
"""Classification:               Unclassified
File Name:                    {prm_filename:s}
Message Purpose:              Request for Predictive Avoidance Support
Message Date/Time (UTC):      {today:%Y %b %d (%j) %H:%M:%S}
Type Windows Requested:       Open
Point of Contact:             Andrei Tokovinin
                              (Voice) +56 51 2205 286
                              (Fax) +56 51 2205 212
                              (E-mail) sampam@ctio.noao.edu
Emergency Phone # at Operations Site: +56 51 2205 500/501
Remarks:                      

MISSION INFORMATION
---------------------------
Owner/Operator:               SOAR
Mission Name/Number:          AURA_SAM_SOAR_355nm_10W_4.46urad_10kHz
Target Type:                  Right Ascension and Declination
Location:                     SOAR_Telescope_at_Cerro_Pachon
Start Date/Time (UTC):        {utstart:%Y %b %d (%j) %H:%M:%S}
End Date/Time (UTC):          {utend:%Y %b %d (%j) %H:%M:%S}
Duration (HH:MM:SS):          {hours:02d}:{minutes:02d}:{seconds:02}

LASER INFORMATION
---------------------------
Laser:                        AURA_SAM_SOAR_355nm_10W_4.46urad_10kHz

SOURCE INFORMATION
------------------------------------
Method:                       Fixed Point
Latitude:                     30.2380 degrees S
Longitude:                    70.7337 degrees W
Altitude:                     2.7380 km

TARGET INFORMATION
------------------------------------
"""

# Target Template =============================================================
target_template = """
Method:                       Right Ascension and Declination
Catalog Date:                 {0.equinox.datetime:%Y}
Right Ascension:              {0.ra.degree:-9.6f}
Declination:                  {0.dec.degree:+9.6f}
"""

# Convert mission date to proper format =======================================
yyyy = args.year
mm = args.month
dd = args.days

utstart = datetime.datetime.strptime(args.utstart, '%H:%M:%S')

utend = datetime.datetime.strptime(args.utend, '%H:%M:%S')

# Does mission starts after UT midnight?
dd1 = dd + 1 if utstart.hour < 12 else dd

# Does mission ends after UT midnight?
dd2 = dd + 1 if utend.hour < 12 else dd

# Setting the UT Times
today = datetime.datetime.utcnow()
utstart = utstart.replace(year=yyyy, month=mm, day=dd1)
utend = utend.replace(year=yyyy, month=mm, day=dd2)

# Format the output -----------------------------------------------------------
# %Y - Four digit year
# %b - short month name with three letters
# %d - zero padded day number
# %j - day of the year
# %H - 24h hour
# %M - zero padded minutes
# %S - zero padded secondss
print(' UTC time now: {:%Y %b %d (%j) %H:%M:%S}'.format(today))
print(' Start Mission: {:%Y %b %d (%j) %H:%M:%S}'.format(utstart))
print(' End Mission: {:%Y %b %d (%j) %H:%M:%S}'.format(utend))

mission_duration = utend - utstart
hours = mission_duration.seconds // 3600
minutes = mission_duration.seconds % 3600 // 60
seconds = mission_duration.seconds % 60

prm_filename = \
    'PRM_AURA_SAM_SOAR_355nm_10W_4.46urad_10kHz_1_' + \
    '{today:%d%b%Y}_For_JDAY{utstart:%j}_RADEC.txt'.format(**locals())

# Fill the template with the previous information
prm = template.format(**locals())

# Reading target file =========================================================
buffer = open(args.targets_filename, 'r')
lines = buffer.readlines()
buffer.close()

number_of_targets = 0

for line in lines:

    # Ignore lines with comments
    if line.startswith('#'):
        continue

    # If line is empty
    if line.isspace():
        continue

    # If coordinates are separated by :
    if ':' in line:
        line_with_single_spaces = " ".join(line.split())
        fields = line_with_single_spaces.split()

        target_name = fields[0]
        right_ascention = fields[1]
        declination = fields[2]
        epoch = fields[3]

    # Or not
    else:
        line_with_single_spaces = " ".join(line.split())
        fields = line_with_single_spaces.split()

        target_name = fields[0]
        right_ascention = ":".join(fields[1:4])
        declination = ":".join(fields[4:7])
        epoch = fields[7]

    # Convert EPOCH to be read by SkyCoord format
    epoch = 'J{:s}'.format(epoch) if 'J' not in epoch else epoch

    # If decimal separator is comma convert to dot
    right_ascention = right_ascention.replace(',', '.')
    declination = declination.replace(',', '.')

    # Create coordinates object
    number_of_targets += 1
    target_coordinates = ' '.join([right_ascention, declination])
    target_coordinates = SkyCoord(
        target_coordinates, unit=(u.hourangle, u.deg), equinox=epoch)

    # Convert to string and add to the PRM file
    target_in_string = target_template.format(target_coordinates)
    prm += target_template.format(target_coordinates)

prm += "\nEND OF FILE"

print('\n Read "{:s}" file.'.format(args.targets_filename))
print(' Number of targets found: {:d} targets'.format(number_of_targets))

# Write the PRM file ==========================================================
prm_file = open(prm_filename, 'w')
prm_file.write(prm)
prm_file.close()
