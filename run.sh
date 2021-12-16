#!/bin/bash -e
# Startup script for Journal Abbreviator app

APPDIR=$HOME/jabbrev
cd $APPDIR
. venv/bin/activate
exec gunicorn -w 1 -b unix:$APPDIR/web.sock --log-file - app:app
