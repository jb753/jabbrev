#!/bin/bash -e
# Startup script for Journal Abbreviator app

. ~/jabbrev/venv/bin/activate
exec gunicorn -w 1 -b unix:/home/jb753/jabbrev/web.sock --log-file - app:app
