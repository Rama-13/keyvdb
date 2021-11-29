#!/bin/sh
gunicorn --workers 1 --worker-class gevent --bind 0.0.0.0:7000 wsgi:app --preload