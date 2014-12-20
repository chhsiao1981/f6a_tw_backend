#!/usr/bin/env python
# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *

import gevent.monkey; gevent.monkey.patch_all()

import multiprocessing

import gunicorn.app.base
from gunicorn.six import iteritems
import mongoengine
import re

import argparse
import sys

from f6a_tw_backend import cfg
from f6a_tw_backend import util
from f6a_tw_backend import wsgi
from f6a_tw_backend import settings


def _number_of_workers():
    return multiprocessing.cpu_count()


class App(gunicorn.app.base.BaseApplication):
    def __init__(self, options=None):
        self.options = options or {}
        self.application = wsgi.application
        super(App, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None and value.__class__.__name__ == 'str'])
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
    (error_code, args) = parse_args()

    error_log = args.error_log or 'log.%s.err.txt' % (args.port)
    access_log = args.access_log or 'log.%s.access.txt' % (args.port)

    cfg.init({'ini_filename': args.ini, 'bind': '0.0.0.0:%s' % (args.port), 'worker_class': 'gevent', 'reload': args.reload, 'errorlog': error_log, 'accesslog': access_log})

    _init_ini_file(args.ini)

    (mongo_host, mongo_port) = util.deserialize_host_port(cfg.config.get('mongo_server_hostname', 'localhost'), default_port=27017)
    mongoengine.connect('f6a_tw_backend', host=mongo_host, port=mongo_port)

    wsgi.init_django_settings_module('f6a_tw_backend.settings')
    wsgi.init_application()

    App(cfg.config).run()


if __name__ == '__main__':
    _main()
