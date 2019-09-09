LogStash CKAN extension
=======================

The LogStash CKAN extension allows to add a `Logstash`_ middleware to the CKAN and stack and optionally configure a LohStash log handler.


This extension builds on top of the previous work of:

* @okfn on https://github.com/okfn/ckanext-sentry.
* @noirbizarre on https://github.com/etalab/ckanext-sentry
* @rshk on https://github.com/opendatatrentino/ckanext-sentry

Installation
------------

To install the extension, activate your virtualenv and run::

    pip install ckanext-logstash

Alternative, you can install a development version with::

    git clone https://github.com/datopian/ckanext-logstash.git
    cd ckanext-logstash
    python setup.py develop
    pip install -r requirements.txt

Configuration
-------------


To activate the plugin, add ``logstash`` to the ``ckan.plugins`` key in your ini file::

    ckan.plugins = logstash <other-plugins>

You must provide a Logstash Endpoint::

    logstash.kind = tcp/udp/amqp
    logstash.host = <hostname>
    logstash.port = <port> (5959 by default)

If you want Logstash to record your log messages, you can turn it on adding the following options::

    logstash.configure_logging=True
    logstash.log_level=WARN

The default log level if not provided in the configuration is INFO.

All these configuration options can also be passed via environment variables:

* ``CKAN_LOGSTASH_KIND``
* ``CKAN_LOGSTASH_HOST``
* ``CKAN_LOGSTASH_PORT``
* ``CKAN_SENTRY_CONFIGURE_LOGGING``
* ``CKAN_SENTRY_LOG_LEVEL``


The configuration also supports env vars named
like the `ckanext-envvars`_ extension convention (eg ``CKAN___LOGSTASH__LOG_LEVEL``).


.. _Logstash: https://www.elastic.co/products/logstash
.. _ckanext-envvars: https://github.com/okfn/ckanext-envvars
