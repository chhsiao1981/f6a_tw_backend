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
    names = ['permit', 'is_valid', 'invalidate_date', 'invalidate_reason', 'valid_date', 'issue_date', 'permit_type', 'old_permit', 'customs_no', 'name', 'en_name', 'indication', 'formulation', 'package', 'type', 'controlled_type', 'main_gradient', 'apply_company', 'apply_address', 'apply_id', 'process_company', 'process_address', 'process_company_address', 'process_company_country', 'procedure', 'change_date', 'usage', 'package2', 'intl_id', 'insurance_id', 'view', 'special', 'color', 'smell', 'mark', 'size', 'memo1', 'memo2']
    df = pd.read_csv(filename, names=names, sep='\t', dtype='object')

    for idx in names:
        df[idx] = df[idx].fillna('')
        df[idx] = df[idx].apply(lambda x: x.decode('utf-8'))

    the_list = util_pd.df_to_dict_list(df)

    '''
    for (idx, each_dict) in enumerate(the_list):
        cfg.logger.debug('to insert: %s: %s', idx, util.json_dumps(each_dict))
    '''

    cfg.logger.debug('to db_insert: the_list: %s', len(the_list))

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
