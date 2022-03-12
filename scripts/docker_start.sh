#!/bin/sh

# gunicorn --chdir app --worker-class eventlet -w 1 run_local:app -b 0.0.0.0:5001
python run_local.py
