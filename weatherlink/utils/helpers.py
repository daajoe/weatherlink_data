# -*- coding: utf-8 -*-
import logging
import logging.config
from os.path import *
import yaml

def read_config(filename=__file__, config_dir=dirname(__file__), config_pattern='%s/../conf/%s.yaml'):
    config_file = config_pattern %(config_dir, splitext(basename(realpath(filename)))[0])
    with open(config_file, 'r') as f:
        return yaml.load(f)

def write_config(data, filename=__file__, config_dir=dirname(__file__), config_pattern='%s/../conf/%s.yaml'):
    config_file = config_pattern % (config_dir, splitext(basename(realpath(filename)))[0])
    with open(config_file, 'w') as f:
        return yaml.dump(data, f)


def setup_logging(filename=__file__,config_dir=dirname(__file__)):
    config_file = '%s/../conf/logging.conf' %config_dir
    logging.config.fileConfig(config_file)
