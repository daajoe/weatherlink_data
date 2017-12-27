#!/usr/bin/false
# -*- coding: utf-8 -*-
#
#
# Copyright 2017
# Johannes K. Fichte
#
# downloader.py is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# downloader.py is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.  You should have received a
# copy of the GNU General Public License along with
# downloader.py.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import

import logging
from itertools import izip
from StringIO import StringIO
from sys import stdin, stdout

import sys
from toolz import merge_with


class MISOutput(object):
    def __init__(self, station_id, dateformat, sensors, ostream=sys.stdout, region='EU'):
        self.__sensors = sensors
        self.__dateformat = dateformat
        self.__station_id = station_id
        self.__ostream = ostream
        if region != 'EU':
            raise NotImplementedError

    def write(self, df):
        header = '<STATION>{station}</STATION><SENSOR>{sensor}</SENSOR><DATEFORMAT>{dateformat}</DATEFORMAT>\n'
        data = '"{date};{time};{value}"\n'
        # "20160922;15:00:00;0.825"

        logging.info("Writing MIS data for sensors %s" %self.__sensors)

        #generate data per sensor
        stream = {}
        for k in self.__sensors:
            logging.debug("Writing data for sensor '%s'" %k)
            stream[k] = StringIO()
            stream[k].write(header.format(station=self.__station_id, sensor=k, dateformat=self.__dateformat))
            # extract from dataframe
            for row in df[['date', 'time', self.__sensors[k]]].itertuples():
                stream[k].write(data.format(date=row[1].replace('-', ''), time="%s:00" % row[2], value=row[3]))

        #write data to outputstream
        for k in self.__sensors:
            self.__ostream.write(stream[k].getvalue())
            self.__ostream.flush()
