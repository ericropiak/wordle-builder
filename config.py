import os

# Due to the limited load balancing algorithm used by gunicorn, 
# it is not possible to use more than one worker process when using socketio
workers = int(os.environ.get('GUNICORN_PROCESSES', '3'))
threads = int(os.environ.get('GUNICORN_THREADS', '1'))

worker_class = 'eventlet'

forwarded_allow_ips = '*'
secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }