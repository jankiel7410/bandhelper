#!/bin/bash
source ~/.virtualenvs/drf/bin/activate

exec gunicorn bandhelper.wsgi -b localhost:8001
