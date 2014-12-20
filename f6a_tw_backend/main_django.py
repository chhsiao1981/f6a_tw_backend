#!/usr/bin/env python
# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *

import gevent.monkey; gevent.monkey.patch_all()

# import multiprocessing

import gunicorn.app.base
from gunicorn.six import iteritems
import mongoengine
import re

import argparse
import sys
import logging

from f6a_tw_backend import cfg
from f6a_tw_backend import util
from f6a_tw_backend import wsgi
from f6a_tw_backend import settings
import uwsgi

application = None

logging.warning('sys.argv: %s', sys.argv)
logging.warning('uwsgi: %s', uwsgi.opt)

def _number_of_workers():
    return 2
    # return multiprocessing.cpu_count()


class App(gunicorn.app.base.BaseApplication):
    def __init__(self, options=None):
        self.options = options or {}
        self.application = wsgi.application
        super(App, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])

        cfg.logger.debug('self.cfg.settings: %s config: %s', self.cfg.settings, config)
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='f6a_tw_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-p', '--port', type=str, required=True, help="port")
    parser.add_argument('-r', '--reload', type=bool, required=False, default=False, help="port")
    parser.add_argument('-e', '--error_log', type=str, required=False, default='', help="error log")
    parser.add_argument('-a', '--access_log', type=str, required=False, default='', help="access log")

    args = parser.parse_args()

    return (S_OK, args)


def _init_ini_file(ini_filename):
    section = 'f6a_tw_backend:django'

    django_settings = cfg.init_ini_file(ini_filename, section)

    for (key, val) in django_settings.iteritems():
        key = key.upper()
        cfg.logger.warning('to set django_settings: key: %s val: %s', key, val)
        setattr(settings, key, val)


def _main():
    global application
    # (error_code, args) = parse_args()

    logging.warning('main_django._main: start')

    opt = uwsgi.opt

    port = opt.get('port', '')
    error_log = opt.get('error_log', 'log.%s.err.txt' % (port))
    access_log = opt.get('access_log', 'log.%s.access.txt' % (port))

    cfg.init({'ini_filename': opt.get('ini', ''), 'bind': '0.0.0.0:%s' % (uwsgi), 'worker_class': 'gevent', 'worker_connections': 10, 'reload': opt.get('reload', False), 'errorlog': error_log, 'accesslog': access_log})

    _init_ini_file(opt.get('ini', ''))

    (mongo_host, mongo_port) = util.deserialize_host_port(cfg.config.get('mongo_server_hostname', 'localhost'), default_port=27017)

    # mongoengine.connect('f6a_tw_backend', host=mongo_host, port=mongo_port)

    wsgi.init_django_settings_module('f6a_tw_backend.settings')
    wsgi.init_application()

    application = wsgi.application

_main()
