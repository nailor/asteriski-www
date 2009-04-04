from nose.tools import eq_ as eq

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User

from asteriski_site.riski_info import models

def test_create_message():
    settings.TEST_TIME = datetime(1983, 11, 1)
    u = User(username='john')
    u.save()

    m = models.Message(
        title='Newsflash!',
        creator=u,
        category=models.INFO,
        content="News! IT'S NEWS!",
        )
    m.save()

    msgs = models.Message.objects.all()
    eq(len(msgs), 1)
    msg = msgs[0]
    eq(msg.created_on, datetime(1983, 11, 1))
    eq(msg.last_modifier, None)
    eq(msg.last_modified_on, None)
    eq(msg.riski_info, True)
    eq(msg.utu_news, True)
    eq(msg.iki_riski, False)


def test_modify_message():
    settings.TEST_TIME = datetime(1983, 11, 1)
    u = User(username='john')
    u.save()

    m = models.Message(
        title='Newsflash!',
        creator=u,
        category=models.INFO,
        content="News! IT'S NEWS!",
        )
    m.save()
    settings.TEST_TIME = datetime(2009, 1, 1)
    m.content = 'Olds!'
    m.save()

    # The last_modifier can't be tested here since it needs requests
    # through the admin interface. Test_admin will handle that
    eq(m.last_modified_on, datetime(2009, 1, 1))

def test_message_to_string():
    u = User(username='john')
    u.save()

    m = models.Message(
        title='Newsflash!',
        creator=u,
        category=models.INFO,
        content="News! IT'S NEWS!",
        )
    m.save()

    eq(unicode(m), u'[INFO] Newsflash!')
