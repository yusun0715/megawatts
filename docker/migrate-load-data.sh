#!/usr/bin/env bash
echo "Migrating database"
python3 manage.py migrate --settings=sitemanagement.settings
python3 manage.py loaddata megawatts/fixtures/load_sites.json --settings=sitemanagement.settings