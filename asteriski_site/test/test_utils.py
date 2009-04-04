from nose.tools import eq_ as eq

from datetime import datetime
from django.conf import settings
from asteriski_site import utils

def test_fake_now():
    settings.TEST_TIME = datetime(2009, 1, 1)
    t = utils.now()
    eq(t, datetime(2009, 1, 1))
