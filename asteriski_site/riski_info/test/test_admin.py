from nose.tools import eq_ as eq, with_setup
from django.test.client import Client
from django.contrib.auth.models import User

from django.conf import settings
from asteriski_site.riski_info.models import (
    Message,
    INFO,
    )

def create_admin():
    u = User.objects.create_user(
        'admin',
        'admin@example.com',
        'password',
        )
    u.is_staff = True
    u.is_superuser = True
    u.save()

@with_setup(setup=create_admin)
def test_message_admin():
    c = Client()
    assert c.login(username='admin', password='password')
    response = c.get('/admin/riski_info/message/')
    eq(response.status_code, 200)

@with_setup(setup=create_admin)
def test_create_message():
    c = Client()
    assert c.login(username='admin', password='password')
    response = c.post(
        '/admin/riski_info/message/add/',
        {
            'title': 'NEWS!',
            'category': INFO,
            'content': 'blahh',
            '_save': 'Save',
            })
    eq(response.status_code, 302)
    msgs = Message.objects.all()
    eq(len(msgs), 1)
    eq(msgs[0].title, 'NEWS!')
    eq(msgs[0].creator.username, 'admin')

