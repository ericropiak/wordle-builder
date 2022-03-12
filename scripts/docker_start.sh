#!/bin/sh

# LOCAL GUNICORN TEST:
# gunicorn --chdir app --worker-class eventlet -w 1 run_local:app -b 0.0.0.0:5001
# PROD IMITATION:
gunicorn --chdir app --worker-class eventlet -w 1 wsgi:application -b 0.0.0.0:8080
# python run_local.py
