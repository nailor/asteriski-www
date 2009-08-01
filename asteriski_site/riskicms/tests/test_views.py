from nose.tools import eq_ as eq, assert_raises

from datetime import datetime

from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import User
from django.test.client import Client
from asteriski_site.riskicms.models import Page
from asteriski_site.riskicms.views import traverse_for_page

def test_path_traversal():
    u = User(username='foo')
    u.save()

    p = Page(
        title='first',
        slug='first',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    p2 = Page(
        parent=p,
        title='second',
        slug='second',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p2.save()

    page = traverse_for_page('/first/second/', Page.objects)
    eq(page.title, 'second')

def test_path_traversal_404_on_special():
    assert_raises(
        Http404,
        traverse_for_page,
        '/__root/',
        Page.objects,
        )

def test_path_traversal_404_on_not_found():
    u = User(username='foo')
    u.save()

    p = Page(
        title='first',
        slug='first',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    p2 = Page(
        parent=p,
        title='second',
        slug='second',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p2.save()

    assert_raises(
        Http404,
        traverse_for_page,
        '/first/third/',
        Page.objects,
        )

def test_path_traversal_404_on_unpublished():
    u = User(username='foo')
    u.save()

    p = Page(
        title='first',
        slug='first',
        content='blah',
        created_by=u,
        last_modified_by=u,
        hidden=True,
        )
    p.save()

    p2 = Page(
        parent=p,
        title='second',
        slug='second',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p2.save()

    assert_raises(
        Http404,
        traverse_for_page,
        '/first/second/',
        Page.online_pages,
        )

def test_view_page():
    u = User(username='foo')
    u.save()

    p = Page(
        title='first',
        slug='first',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    c = Client()
    response = c.get('/first/')
    eq(response.status_code, 200)

    assert 'first' in response.content
    assert 'blah' in response.content
