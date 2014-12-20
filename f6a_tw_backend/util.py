# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *

import os
import random
import math
import uuid
import base64
import time
import ujson as json
import pytz
from calendar import timegm
import arrow
from subprocess import Popen, PIPE
import string

from f6a_tw_backend import cfg


##########
# mongo
##########
def db_find_one(db_name, key, fields=None):
    (error_code, error_msg, result) = db_find_one_e(db_name, key, fields)

    return result


def db_find_one_e(db_name, key, fields=None):
    if fields is None:
        fields = {'id': False}

    error_code = S_OK
    error_msg = ''

    result = {}
    try:
        result = cfg.config.get(db_name).find_one(key, fields=fields)
        result = dict(result)
    except Exception as e:
        cfg.logger.error('unable to db_find_one: db_name: %s e: %s', db_name, e)
        error_code = S_ERR
        error_msg = 'unable to db_find_one: db_name: %s e: %s' % (db_name, e)
        result = {}

        _db_restart_mongo(db_name, e)

    if not result:
        result = {}

    return (error_code, error_msg, result)


def db_find(db_name, key=None, fields=None):
    (error_code, error_msg, result) = db_find_e(db_name, key, fields)

    return result


def db_find_e(db_name, key=None, fields=None):
    if fields is None:
        fields = {'_id': False}

    error_code = S_OK
    error_msg = ''

    try:
        db_result_it = db_find_it(db_name, key, fields)
        result = list(db_result_it)
    except Exception as e:
        cfg.logger.error('unable to db_find: db_name: %s e: %s', db_name, e)

        error_code = S_ERR
        error_msg = 'unable to db_find: db_name: %s e: %s' % (db_name, e)
        result = []

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, result)


def db_find_it(db_name, key=None, fields=None):
    (error_code, error_msg, result) = db_find_it(db_name, key, fields)

    return result


def db_find_it_e(db_name, key=None, fields=None):
    error_code = S_OK
    error_msg = ''

    result = []
    try:
        if key is None:
            result = cfg.config.get(db_name).find(fields=fields)
        else:
            result = cfg.config.get(db_name).find(key, fields=fields)
    except Exception as e:
        cfg.logger.error('unable to db_find_it: db_name: % key: %s', db_name, key)

        error_code = S_ERR
        error_msg = 'unable to db_find_it: db_name: %s key: %s' % (db_name, key)
        result = None

        _db_restart_mongo(db_name, e)

    if not result:
        result = []

    return (error_code, error_msg, result)


def db_insert(db_name, val):
    (error_code, error_msg, result) = db_insert_e(db_name, val)

    return result


def db_insert_e(db_name, val):
    error_code = S_OK
    error_msg = ''

    if not val:
        cfg.logger.error('db_name: %s no val: val: %s', db_name, val)
        return (S_ERR, 'no val')

    result = []
    try:
        result = cfg.config.get(db_name).insert(val, manipulate=False, ordered=False)
    except Exception as e:
        cfg.logger.error('unable to insert: db_name: %s e: %s', db_name, e)
        result = []
        error_code = S_ERR
        error_msg = 'unable to insert: db_name: %s e: %s' % (db_name, e)

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, result)


def db_update(db_name, key, val, is_set=True, upsert=True, multi=True):
    (error_code, error_msg, result) = db_update_e(db_name, key, val, is_set=is_set, upsert=upsert, multi=multi)

    return result


def db_update_e(db_name, key, val, is_set=True, upsert=True, multi=True):
    if not key or not val:
        cfg.logger.error('no key or val: db_name: %s', db_name)
        return (S_ERR, "no key or val: db_name: %s" % (db_name), {})

    return db_force_update_e(db_name, key, val, is_set=is_set, upsert=upsert, multi=multi)


def db_force_update(db_name, key, val, is_set=True, upsert=True, multi=True):
    (error_code, error_msg, result) = db_force_result_e(db_name, key, val, is_set=is_set, upsert=upsert, multi=multi)

    return result


def db_force_update_e(db_name, key, val, is_set=True, upsert=True, multi=True):
    error_code = S_ERR
    error_msg = ''

    if is_set:
        val = {"$set": val}

    result = {}
    try:
        result = cfg.config.get(db_name).update(key, val, upsert=upsert, multi=multi)
        error_code = S_OK
    except Exception as e:
        cfg.logger.error('unable to db_update: db_name: %s key: %s e: %s', db_name, key, e)
        error_code = S_ERR
        error_msg = 'unable to db_update: db_name: %s e: %s' % (db_name, e)
        result = {}

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, result)


def db_save(db_name, doc):
    (error_code, error_msg, result) = db_save_e(db_name, doc)

    return result


def db_save_e(db_name, doc):
    error_code = S_OK
    error_msg = ''

    if not doc:
        cfg.logger.error('no doc')
        error_msg = 'no doc: db_name: %s' % (db_name)
        return (S_ERR, error_msg, {})

    result = {}
    try:
        result = cfg.config.get(db_name).save(doc)
    except Exception as e:
        cfg.logger.error('unable to save: db_name: %s doc: %s e: %s', db_name, doc, e)
        _db_restart_mongo(db_name, e)

        error_code = S_ERR
        error_msg = 'unable to save: db_name: %s doc: %s e: %s' % (db_name, doc, e)
        result = {}

    return (error_code, error_msg, result)


def db_remove(db_name, key):
    (error_code, error_msg, result) = db_remove_e(db_name, key)

    return result


def db_remove_e(db_name, key):
    error_code = S_OK
    error_msg = ''

    if not key:
        cfg.logger.error('no key: db_name: %s key: %s', db_name, key)
        error_msg = 'no key: db_name: %s' % (db_name)
        return (error_code, error_msg, {})

    return db_force_remove_e(db_name, key=key)


def db_force_remove(db_name, key=None):
    (error_code, error_msg, result) = db_force_remove_e(db_name, key)

    return result


def db_force_remove_e(db_name, key=None):
    if key is None:
        key = {}

    error_code = S_OK
    error_msg = ''

    result = {}
    try:
        result = cfg.config.get(db_name).remove(key)
    except Exception as e:
        cfg.logger.error('unable to remove: db_name: %s key: %s', db_name, key)
        result = {}
        error_code = S_ERR
        error_msg = 'unable to remove: db_name: %s key: %s' % (db_name, key)

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, result)


def db_distinct(db_name, distinct_key, query_key, fields=None):
    (error_code, error_msg, result) = db_distinct_e(db_name, distinct_key, query_key, fields)

    return result


def db_distinct_e(db_name, distinct_key, query_key, fields=None):
    if fields is None:
        fields = {'_id': False}

    error_code = S_OK
    error_msg = ''

    results = []
    try:
        db_result = cfg.config.get(db_name).find(query_key, fields=fields)
        results = db_result.distinct(distinct_key)
    except Exception as e:
        cfg.logger.error('unable to db_distinct: db_name: %s query_key: %s distinct_key: %s e: %s', db_name, query_key, distinct_key, e)
        error_code = S_ERR
        error_msg = 'unable to db_distinct: db_name: %s query_key: %s distinct_key: %s e: %s' % (db_name, query_key, distinct_key, e)
        results = []

        _db_restart_mongo(db_name, e)

    return results


def db_find_and_modify(db_name, key, val, is_set=True, upsert=True, multi=True):
    (error_code, error_msg, result) = db_find_and_modify_e(db_name, key, val, is_set=is_set, upsert=upsert, multi=multi)

    return result


def db_find_and_modify_e(db_name, key, val, is_set=True, upsert=True, multi=True):
    error_code = S_OK
    error_msg = ''

    if is_set:
        val = {'$set': val}

    result = None
    try: 
        result = cfg.config.get(db_name).find_and_modify(key, val, upsert=upsert, multi=multi)
    except Exception as e: 
        cfg.logger.error('unable to db_find_and_modify: db_name: %s key: %s val: %s e: %s', db_name, key, val, e)
        result = None
        error_code = S_ERR
        error_msg = 'unable to db_find_and_modify: db_name: %s key: %s val: %s e: %s' % (db_name, key, val, e)

        _db_restart_mongo(db_name, e)

    if result is None:
        result = {}

    return dict(result)


def db_aggregate_it(db_name, pipe):
    (error_code, error_msg, result) = db_aggregate_it_e(db_name, pipe)

    return result


def db_aggregate_it_e(db_name, pipe):
    error_code = S_OK
    error_msg = ''

    db_result = []
    try:
        db_result = cfg.config.get(db_name).aggregate(pipeline=pipe, cursor={}, allowDiskUse=True)
    except Exception as e:
        cfg.logger.error('unable to db_aggregate_it: db_name: %s pipe: %s e: %s', db_name, pipe, e)
        db_result = []
        error_code = S_ERR
        error_msg = 'unable to db_aggregate_it: db_name: %s pipe: %s e: %s' % (db_name, pipe, e)

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, db_result)


def db_aggregate(db_name, pipe):
    (error_code, error_msg, result) = db_aggregate_e(db_name, pipe)

    return result


def db_aggregate_e(db_name, pipe):
    error_code = S_OK
    error_msg = ''

    (error_code, error_msg, db_result) = db_aggregate_it_e(db_name, pipe)
    if error_code != S_OK:
        return (error_code, error_msg, [])

    result = []
    try:
        result = list(db_result)
    except Exception as e:
        cfg.logger.error('unable to db_aggregate: db_name: %s pipe: %s e: %s', db_name, pipe, e)
        result = []
        error_code = S_ERR
        error_msg = 'unable to db_aggregate: db_anme: %s pipe: %s e: %s' % (db_name, pipe, e)

        _db_restart_mongo(db_name, e)

    return (error_code, error_msg, result)


def db_aggregate_parse_results(db_results):
    return [db_aggregate_parse_result(db_result) for db_result in db_results]


def db_aggregate_parse_result(db_result):
    result = {key: val for (key, val) in db_result.iteritems() if key != '_id'}
    result.update(db_result['_id'])

    return result


def db_largest(db_name, key, query, group_columns=None):
    db_results = db_largest_list(db_name, key, query, group_columns)
    if not db_results:
        return {}

    return db_results[0]


def db_largest_list(db_name, key, query, group_columns=None):
    '''
    key: key for max
    query: query
    group_columns: columns for grouping
    '''
    if group_columns is None:
        group_columns = query.keys()

    group = {}
    group['max'] = {'$max': '$' + key}
    group['_id'] = {column: '$' + column for column in group_columns}
    pipe = [
        {'$match': query},
        {'$group': group},
    ]

    cfg.logger.debug('to db_aggregate: pipe: %s', pipe)
    results = db_aggregate(db_name, pipe)

    cfg.logger.debug('after db_aggregate: results: %s', results)

    return results


def _db_restart_mongo(db_name, e):
    e_str = str(e)

    # ignore dup error
    if re.search('^E11000', e_str):
        return

    cfg._init_mongo()


##########
# type 
##########
def _str(item, encoding='utf-8', default=''):
    if item.__class__.__name__ == 'unicode':
        try:
            result = item.encode(encoding)
        except Exception as e:
            result = default
        return result

    try:
        result = str(item)
    except Exception as e:
        result = default
    return result


def _unicode(item, encoding='utf-8', default=u''):
    if item.__class__.__name__ == 'unicode':
        return item

    return _str(item).decode(encoding)


def _int(item, default=0):
    if item == 'null':
        return 0

    if item == 'false':
        return 0

    if item == 'true':
        return 1

    result = default
    try:
        result = int(item)
    except Exception as e:
        # cfg.logger.error('unable to _int: item: %s, default: %s e: %s', item, default, e)
        result = default

    return result


def _float(item, default=0.0):
    if item == 'null':
        return 0.0

    if item == 'false':
        return 0.0

    if item == 'true':
        return 1.0

    result = default
    try:
        result = float(item)
    except Exception as e:
        # cfg.logger.error('unable to _float: item: %s, default: %s e: %s', item, default, e)
        result = default

    return result


def _bool(item):
    if item == 'true':
        return True
    
    if item == 'True':
        return True

    if item == True:
        return True

    if item == 'false':
        return False

    if item == 'False':
        return False

    if item == False:
        return False

    return False if not item else True


##########
# timestamp
##########
def timestamp_to_datetime(the_timestamp):
    the_float_sec_timestamp = timestamp_to_float_sec_timestamp(the_timestamp)
    return datetime.utcfromtimestamp(the_float_sec_timestamp)


def sec_timestamp_to_datetime(the_sec_timestamp):
    the_sec_timestamp = _int(the_sec_timestamp)
    return datetime.utcfromtimestamp(the_sec_timestamp)


def timestamp_to_sec_timestamp(the_timestamp):
    return _int(the_timestamp / 1000)


def timestamp_to_float_sec_timestamp(the_timestamp):
    return _float(the_timestamp) / 1000.0


def get_timestamp():
    return _int(time.time() * 1000)


def get_sec_timestamp():
    return _int(time.time())


def get_hr_timestamp():
    the_hr_sec_timestamp = get_hr_sec_timestamp()
    return the_hr_sec_timestamp * 1000


def get_hr_sec_timestamp():
    the_sec_timestamp = get_sec_timestamp()
    the_hr_sec_timestamp_block = the_sec_timestamp // 3600
    the_hr_sec_timestamp = the_hr_sec_timestamp_block * 3600

    return the_hr_sec_timestamp


def timestamp_to_day_timestamp(the_timestamp):
    the_sec_timestamp = timestamp_to_sec_timestamp(the_timestamp)
    day_sec_timestamp = sec_timestamp_to_day_timestamp(the_sec_timestamp)
    return day_sec_timestamp * 1000


def sec_timestamp_to_day_timestamp(the_sec_timestamp):
    the_block = the_timestamp // 86400
    return the_block * 86400


##########
# http
##########
def http_multipost(the_url_data, timeout=HTTP_TIMEOUT, cookies=None):
    '''
    the_url_data: {the_url: data_by_url}
    '''
    the_urls = the_url_data.keys()
    the_url_data_list = [(each_url, the_url_data[each_url]) for each_url in the_urls]

    result_list = http_multipost_list(the_url_data_list, timeout=timeout, cookies=cookies)

    if not result_list:
        return {}

    result = {each_result[0]: each_result[1] for each_result in result_list}

    return result


def http_multipost_list(the_url_data, timeout=HTTP_TIMEOUT, cookies=None):
    '''
    the_url_data: [(the_url, data_by_url)]
    '''
    rs = (grequests.post(each_url_data[0], data=each_url_data[1], timeout=timeout, cookies=cookies) for each_url_data in the_url_data)
    result_map = grequests.map(rs)

    result = []
    try:
        result_map_content = [_grequest_get_content(each_result_map) for each_result_map in result_map]
        result = [(each_url_data[0], result_map_content[idx]) for (idx, each_url_data) in enumerate(the_url_data)]
    except Exception as e:
        cfg.logger.error('unable to http_multipost: the_url_data: %s e: %s', the_url_data, e)
        result = []
    return result


def http_multiget(the_urls, timeout=HTTP_TIMEOUT, cookies=None):
    '''
    the_urls: [the_url]
    '''
    rs = (grequests.get(u, timeout=timeout, cookies=cookies) for u in the_urls)
    result_map = grequests.map(rs)
    try:
        result_map_text = [_grequest_get_content(each_result_map) for each_result_map in result_map]
        result = {the_url: result_map_text[idx] for (idx, the_url) in enumerate(the_urls)}
    except Exception as e:
        cfg.logger.error('unable to http_multiget: the_urls: %s e: %s', the_urls, e)
        result = {}

    return result


def _grequest_get_content(result):
    if result is None:
        return ''

    return getattr(result, 'content', '')


##########
# json
##########
def json_dumps(json_struct, default='', indent=None):
    result = ''
    try:
        result = json.dumps(json_struct)
    except Exception as e:
        cfg.logger.error('unable to json_dumps: json_struct: %s e: %s', json_struct, e)
        result = default

    return result


def json_loads(json_str, default={}):
    result = default
    try:
        result = json.loads(json_str)
    except Exception as e:
        cfg.logger.error('unable to json_loads: json_str: %s e: %s', json_str, e)
        result = default

    return result


##########
# sys
##########

def makedirs(dir_name):
    try:
        os.makedirs(dir_name)
    except Exception as e:
        cfg.logger.error('unable to makedirs: dir_name: %s e: %s', dir_name, e)


def process_cmd(cmd, is_stdout=True, is_stderr=True, is_wait=True):
    output_content = ''
    output_stderr = ''
    process = None

    the_stdout = PIPE if is_stdout else None
    the_stderr = PIPE if is_stderr else None
    process = Popen(cmd, stdout=the_stdout, stderr=the_stderr)

    if is_wait:
        (output_content, output_stderr) = process.communicate()
        cfg.logger.warning('cmd done: output_content: %s', output_content)

    return (process, output_content, output_stderr)


##########
# misc
##########

def gen_random_string(length=40):
    rand_str = string.ascii_letters + string.digits + '-_'
    the_str = uuid.uuid4().hex
    rand_len = max(length - len(the_str), 0)
    return the_str + ''.join(random.choice(the_str) for i in range(rand_len))


def deserialize_host_port(hostname, default_port=None):
    if not default_port:
        default_port = 0

    port = default_port

    the_list = hostname.split(':')
    if len(the_list) < 2:
        return (hostname, default_port)

    return (host, port)
