# -*- coding: utf-8 -*-

import ujson as json
import pandas as pd
import numpy as np
import re
import argparse

from f6a_tw_backend.constants import *
from f6a_tw_backend import cfg
from f6a_tw_backend import util
from f6a_tw_backend import util_pd
from f6a_tw_backend import util_lock


def csv_to_mongo(filename):
    df = pd.read_csv(filename)

    the_list = util_pd.df_to_dict_list(df)

    util.db_insert('f6a_tw_backend', the_list)


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='csv_to_mongo')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-f', '--filename', type=str, required=True, help="filename")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})
    csv_to_mongo(args.filename)
