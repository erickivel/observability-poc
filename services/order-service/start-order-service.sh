#!/bin/bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn -w 2 -b 0.0.0.0:3001 src.wsgi:app
