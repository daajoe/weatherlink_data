#!/usr/bin/false
# -*- coding: utf-8 -*-
#

import datetime
import httplib
import itertools
from itertools import izip
import logging
import struct
import sys

import measures


class Downloader(object):
    def __init__(self, username, password, fields, region='US'):
        self.username = username
        self.password = password
        self.fields = fields
        self.format_mapper = measures.format_map[region]

    @staticmethod
    def timestamp(t):
        """
        Takes a datetime.datetime object and returns corresponding integer
        necessary in request to retrieve data. This value is effectively
        just the two byte date stamp followed by the two byte time stamp.
        >>> import datetime
        >>> tstamp(datetime.datetime(2012, 6, 17, 15, 5)) # 6/17/12 15:05
        416351713
        >>> tstamp(None)
        0
        """
        if t is None:
            return 0
        vantageTimeStamp = (100 * t.hour) + t.minute
        vantageDateStamp = t.day + (t.month << 5) + ((t.year - 2000) << 9)
        return (vantageDateStamp << 16) + vantageTimeStamp

    # TODO: replace print by proper logging
    def retrieveData(self, conn, timestamp):
        """
        returns an httplib.HTTPReponse object containing the requested
        data from weatherlink.com after time timestamp.
        """
        # TODO: replace
        url = "/webdl.php?timestamp=" + str(timestamp) + "&user=" + self.username + "&pass=" + \
              self.password + "&action="

        conn.request("GET", url + "headers")  # request with action=headers
        res = conn.getresponse()
        # print res.getheaders()
        # print res.read()
        # exit(1)

        if res.status != 200:
            print >> sys.stderr, "Could not access weatherlink server."
            print >> sys.stderr, "HTTP status code: %s: %s" % res.status, res.reason
            exit(1)

        # parse out number of records
        numRecords = res.read().split("\n")[1].split("=")[1]

        logging.info("Preparing to import %s records..." % numRecords)
        conn.request("GET", url + "data")  # request with action=data
        res = conn.getresponse()
        logging.info("Headers requested.")

        if res.status != 200:
            print >> sys.stderr, "Could not retrieve data from server."
            print >> sys.stderr, "HTTP status code: %s: %s" % res.status, res.reason
            exit(1)
        # print res, dir(res)
        # print res.getheaders()
        return res, int(numRecords)

    def appendRecord(self, record, mask, europe=True):
        """
        append the appropriate data from the 52 byte record onto the
        provided local CSV file. This function handles unpacking the
        data and interpreting the bytes.
        """
        if record == measures.DASHED:
            print >> sys.stderr, "Skipping dashed record."
            return
        # unpack 52 byte record into 39 data values
        vals = struct.unpack(measures.fmtA, record)
        # delete vals listed in dotfile
        vals = list(itertools.compress(vals, mask))
        recordDict = {f: self.format_mapper[f](v) for f, v in izip(self.fields, vals)}
        return recordDict

    def retrieve_data(self, timestamp=datetime.datetime(1970, 1, 1)):
        # Create mask to delete unnecessary data in appendRecord()
        mask = [0 if field not in self.fields else 1 for field in measures.ordFieldsA]

        # Handle CSV setup, return timestamp (timestamp of most recent record on file)
        # convert datetime.datetime timestamp to WeatherLink format
        timestamp = self.timestamp(timestamp)

        # Retrieve all records more recent than timestamp
        conn = httplib.HTTPConnection("weatherlink.com")
        res, numRecords = self.retrieveData(conn, timestamp)

        last_modified = res.getheader('date')
        # last_modified = res.info().get('last-modified')

        records = []

        logging.info("Retrieving records...")
        # Read each retrieved 52 byte record and append it to the CSV file
        for i in range(numRecords):
            record = res.read(52)
            record = self.appendRecord(record, mask)
            if record:
                records.append(record)

        logging.info("Done.")
        conn.close()

        #check age of records the weatherlink API is problematic due to the 1h delay of archive data
        # it = next(iterator(records))
        # while
        # for record in records:
        # print records[0]['time']
        # print records[-1]['time']
        #
        # print last_modified
        # exit(1)
        return records, last_modified #, last_data
