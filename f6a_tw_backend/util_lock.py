# -*- coding: utf-8 -*-

import gevent
from f6a_tw_backend.constants import *

from f6a_tw_backend import cfg
from f6a_tw_backend import util


def lock(lock_key, lock_db='lock', lock_expire_time=0, block_time_out=0, time_sleep=100):
    '''
    lock_key: key to lock
    lock_db: underlying mongo db to lock (require ensure unique on "key")
    lock_expire_time: expire time from current timestamp (in milliseconds)
    block_time_out: time out of trying to lock (in milliseconds)
    time_sleep: sleep when retrying lock (in milliseconds)
    '''
    start_timestamp = util.get_timestamp()
    while True:
        current_timestamp = util.get_timestamp()
        locker = util.db_find_one(lock_db, {"key": lock_key})
        expire_time = locker.get('expire_time', 0)
        if locker and expire_time and current_timestamp > expire_time:
            unlock(lock_db, lock_key, locker.get('seq', 0))

        seq = locker.get('seq', 0)
        seq += 1

        expire_timestamp = 0 if not lock_expire_time else current_timestamp + lock_expire_time

        (error_code, error_msg, db_result) = util.db_insert2(lock_db, {"key": lock_key, "seq": seq, "expire_time": expire_timestamp})
        if error_code == S_OK:
            return (S_OK, '', {"key": lock_key, "seq": seq})

        if block_time_out >= 0 and current_timestamp >= start_timestamp + block_time_out:
            return (S_ERR, "already locked", {})

        gevent.sleep(time_sleep / 1000)


def refresh(lock_key, seq, lock_db='lock', lock_expire_time=0):
    the_timestamp = util.get_timestamp()
    expire_timestamp = 0 if not lock_expire_time else the_timestamp + lock_expire_time

    (error_code, error_msg, db_result) = util.db_update2(lock_db, {"key": lock_key, "seq": seq}, {"expire_time": expire_timestamp}, upsert=False)

    if error_code != S_OK:
        return (error_code, error_msg)

    return (S_OK, "")


def unlock(lock_key, seq, lock_db='lock'):
    (error_code, error_msg, db_result) = util.db_remove2(lock_db, {"key": lock_key, "seq": seq})
    if error_code != S_OK:
        return (error_code, error_msg)
    return (S_OK, "")
