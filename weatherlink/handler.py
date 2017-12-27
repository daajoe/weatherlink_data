#!/usr/bin/env python
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

from collections import OrderedDict
from cStringIO import StringIO
import datetime
import logging
import pandas as pd
import os

import weatherlink.data.downloader
from weatherlink.exporter.mis_export import MISOutput

__author__ = 'Johannes K. Fichte'
__license__ = 'GPL3+'
__version__ = '1.0.0'

fields = 'date,time,out_temp,hi_out_temp,low_out_temp,rainfall,hi_rain_rate,barometer,' \
         'solar_rad,num_wind_samples,inside_temp,in_humidity,out_humidity,avg_wind,hi_wind,' \
         'hi_wind_dir,prevailing_dir,avg_UV,ET,high_solar_rad,high_UV,forecast_rule,leaf_temp1,' \
         'leaf_temp2,leaf_wet1,leaf_wet2,soil_temp1,soil_temp2,soil_temp3,soil_temp4,extra_hum1,' \
         'exta_hum2,extra_temp1,extra_temp2,extra_temp3'.split(',')


# TODO: remember what's been imported already; store last import
# TODO: fun export to elastic search, vizualize with kibana
class Handler(object):
    def __init__(self, username, password, fields, region, csv_prefix="./fhof",
                 last_updated=None, mis_infos=None):
        self.username = username
        self.password = password
        self.fields = fields
        self.region = region
        self.csv_prefix = csv_prefix
        self.last_updated = last_updated if last_updated else datetime.datetime(1970, 1, 1)
        self.mis_infos = mis_infos
        # TODO: parameter for continously

    def output_daily_csv(self, df, increment=True):
        df = df[fields]
        for group in df.groupby(['date']):
            filename = self.incremented_filename(group[0], increment, "csv")
            if not os.path.isfile(filename):
                logging.info("Writing to '%s'." % filename)
                sorted_group = group[1].sort_values(by=['date', 'time'])
                sorted_group.to_csv(filename, index=False, header='column_names')
            else:
                logging.info("File already exists '%s'." % filename)
                logging.info("Reading old data...")
                df_disk = pd.read_csv(filename)
                logging.info("Merging...")
                df_new = pd.concat([df_disk, df]).drop_duplicates().reset_index(drop=True)
                logging.info("Appending to '%s'." % filename)
                sorted_group = df_new[fields].sort_values(by=['date', 'time'])
                sorted_group.to_csv(filename, index=False, header='column_names')

    def output_continous_mis(self, df, increment=True):
        for group in df["date"].unique():
            filename = self.incremented_filename(group, increment, "mis")
            with open(filename, 'w') as fh:
                o = MISOutput(station_id=self.mis_infos['id'], dateformat=self.mis_infos['dateformat'],
                              sensors=self.mis_infos['sensors'], ostream=fh, region=self.region)
                o.write(df[(df["date"] == group)])

    def incremented_filename(self, group, increment, extension='mis'):
        fname = lambda i: "%s-%s%s.%s" % (os.path.realpath(os.path.expanduser(self.csv_prefix)), group, i, extension)
        filename = fname("")
        if increment:
            i = 0
            filename = fname("_%s" % i)
            while os.path.isfile(filename):
                filename = fname("_%s" % i)
                i += 1
        return filename

    def run(self):
        # TODO: run in daily mail mode only
        # keep the dict here for a while to be backwards compatible
        dl = weatherlink.data.Downloader(self.username, self.password, self.fields, self.region)
        # read last input
        data, last_modified = dl.retrieve_data(self.last_updated)
        # daily csv file
        logging.info("Converting data")
        # print data
        # TODO: next here
        df = pd.DataFrame(data)
        increment = True
        self.output_daily_csv(df, increment=increment)
        # TODO: move to output handler
        self.output_continous_mis(df, increment=increment)

        # convert to mis
        # move mis file to make operation atomar
        # write update mis latest file

        # update last written
        # sendmail
        return last_modified

    def mail(self):
        pass

        # Datum: Sat Oct 22 22:00:08 CEST 2016
        # bz2
        # echo 'Datum:' $(date) | mailx -s 'Davis Wetterdaten (fortlaufend)' -A $outputfile.bz2
        # johannes.fichte@gmail.com lorenz.fichte@googlemail.com klaus-dieter@fichteweb.de
        # bzip2 -k $outputfile
