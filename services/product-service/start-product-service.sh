#!/bin/bash
# NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn -w 2 -b 0.0.0.0:3002 src.wsgi:app
NEW_RELIC_CONFIG_FILE=services/product-service/newrelic.ini newrelic-admin run-program gunicorn --chdir services/product-service -w 2 -b 0.0.0.0:3002 src.wsgi:app
