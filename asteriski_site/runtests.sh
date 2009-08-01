#!/bin/sh

export DJANGO_SETTINGS_MODULE=testsettings
nosetests --with-django $*


