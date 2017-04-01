#!/usr/bin/env bash
su -m django -c "python3 manage.py runserver 0.0.0.0:8002 --settings=sitemanagement.settings"