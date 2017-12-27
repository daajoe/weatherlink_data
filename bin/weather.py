#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

__version__ = '1.0.0'

import argparse
import os
import sys

from weatherlink.data import measures
from weatherlink.data.downloader import Downloader
from weatherlink.exporter.csv_export import CSVOutput


def optionSetup():
    """ 
    Use optparse module to setup the program's command line options
    and defaults. The funtion returns the tuple (options, args) 
    where options.filename is the provided filename, etc.
    """

    parser = argparse.ArgumentParser(description="%(prog)s -f instance")
    parser.add_argument("-v", action="version", version="%(prog)s {version}".format(version=__version__))
    parser.add_argument("-f", "--file", dest="filename", action="store", type=lambda x: os.path.realpath(x),
                        help="csv file to store data", default=os.path.expanduser("~/weatherlink.csv"))
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout")
    parser.add_argument("-m", "--measure", action="store", dest="measures", default="US",
                        help="use the following measure", choices=measures.format_map.keys())

    args = parser.parse_args()
    return args


def readSettings(filename):
    """
    Read the client's weatherlink.com account username, password,
    and list of fields to exclude.
    """
    try:
        f = open(filename, 'r')  # open in append binary mode
    except IOError as err:
        print >> sys.stderr, "Issue opening file: %s", filename
        print >> sys.stderr, err
        exit(1)
    with f:
        username = f.readline().strip()
        password = f.readline().strip()
        exclusions = f.read()
        exclusions = "".join(exclusions.split()).split(',')
        fields = [f for f in measures.ordFieldsA if f not in exclusions]
        return username, password, fields


def main():
    options = optionSetup()
    (username, password, fields) = readSettings("%s/.weatherlink" % os.getenv("HOME"))
    output = CSVOutput(options.filename, fields)
    timestamp = output.initCSV()

    downloader = Downloader(username, password, fields, region=options.measures)
    data, _ = downloader.retrieve_data(timestamp)
    output.write_data(data)


if __name__ == '__main__':
    main()
