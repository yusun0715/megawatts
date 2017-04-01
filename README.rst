Site Management

Documentation

Getting started
This repository is for site management. It uses an architecture design pattern called
dependency injection. This is specifically useful for constructing unittests.
It will only expose a "logic" object which corresponds to the idea of encapsulation.


Docker

Run in Docker Linux

- ``docker-compose build``
- ``docker-compose up -d``
- ``docker-compose run sitemanagement bin/run_test_with_coverage.sh``
- ``docker-compose run sitemanagement python manage.py test --settings=sitemanagement.settings``

You can connect to the application by visiting http://localhost:8002/sites
Replacing the test command with any other manage.py command will work as well.