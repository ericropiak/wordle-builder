#!/bin/sh

gunicorn --chdir app --log-level INFO main:app
# python run_local.py
