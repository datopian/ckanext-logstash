# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import logstash

from ckan import plugins


log = logging.getLogger(__name__)


CONFIG_FROM_ENV_VARS = {
    'logstash.kind': 'CKAN_LOGSTASH_KIND',
    'logstash.host': 'CKAN_LOGSTASH_HOST',
    'logstash.port': 'CKAN_LOGSTASH_PORT',
    'logstash.configure_logging': 'CKAN_LOGSTASH_CONFIGURE_LOGGING',
    'logstash.log_level': 'CKAN_LOGSTASH_LOG_LEVEL',
}


class LogstashPlugin(plugins.SingletonPlugin):
    '''A simple plugin that add the Logstash middleware to CKAN'''
    plugins.implements(plugins.IMiddleware, inherit=True)

    def make_middleware(self, app, config):
        if plugins.toolkit.check_ckan_version('2.3'):
            return app
        else:
            self._configure_logging(config)
            return app

    def _configure_logging(self, config):
        '''
        Configure the Logstash log handler to the specified level
        '''
        logstash_host = config.get('logstash.host')
        logstash_port = config.get('logstash.port') or 5959
        logstash_kind = config.get('logstash.kind')
        logstash_kind = logstash_kind or ''
        logstash_kind = logstash_kind.lower()
        if logstash_kind == 'tcp':
            handler = logstash.TCPLogstashHandler(
                logstash_host, logstash_port, version=1
            )
        elif logstash_kind == 'udp':
            handler = logstash.LogstashHandler(
                logstash_host, logstash_port, version=1
            )
        elif logstash_kind == 'ampq':
            handler = logstash.AMQPLogstashHandler(
                host=logstash_host,  version=1
            )
        else:
            log.warning('Unknown logstash kind specified (%s)',
                        config.get('logstash.kind'))
            return

        handler.setLevel(logging.NOTSET)
        handler.formatter.host = config.get('ckan.site_url')

        loggers = ['', 'ckan', 'ckanext', 'logstash.errors']
        logstash_log_level = config.get('logstash.log_level', logging.INFO)
        for name in loggers:
            logger = logging.getLogger(name)
            logger.addHandler(handler)
            logger.setLevel(logstash_log_level)

        log.debug('Setting up Logstash logger with level {0}'.format(
            logstash_log_level))
