#!/bin/bash
source ~/.virtualenvs/bandhelper3/bin/activate

exec gunicorn bandhelper.wsgi -b localhost:8001
