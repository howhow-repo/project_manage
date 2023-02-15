# -*- encoding: utf-8 -*-
bind = '0.0.0.0:80'
workers = 2
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True

# run gunicorn by:
# $ gunicorn -c gunicorn-cfg.py core.wsgi:application
