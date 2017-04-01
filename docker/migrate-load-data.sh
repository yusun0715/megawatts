#!/usr/bin/env bash
echo "Migrating database"
python3 manage.py migrate --settings=sitemanagement.settings