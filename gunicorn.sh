#!/bin/bash
source ~/.virtualenvs/bandhelper/bin/activate

exec gunicorn bandhelper.wsgi -b localhost:8001
