#!/bin/bash
source ~/.virtualenvs/bandhelper/bin/activate

gunicorn bandhelper.wsgi -b localhost:8001
