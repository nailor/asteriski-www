from nose.tools import eq_ as eq, assert_raises

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from asteriski_site.riskicms.models import Page

def test_manager_unpublished_page():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1999, 1, 2),
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    eq(Page.online_pages.all().count(), 0)

def test_manager_hidden_page():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1998, 1, 2),
        created_by=u,
        last_modified_by=u,
        hidden=True,
        )
    p.save()

    eq(Page.online_pages.all().count(), 0)

def test_manager_expired_page():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1998, 1, 2),
        created_by=u,
        last_modified_by=u,
        expire_time=datetime(1998, 12, 30),
        )
    p.save()

    eq(Page.online_pages.all().count(), 0)

def test_manager_published_page():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1998, 1, 2),
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    eq(Page.online_pages.all().count(), 1)

def test_manager_published_page_with_expire_time():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1998, 1, 2),
        expire_time=datetime(2000, 1, 1),
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    eq(Page.online_pages.all().count(), 1)

def test_page_unicode_representation():
    settings.TEST_TIME = datetime(1999, 1, 1)
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        publish_time=datetime(1998, 1, 2),
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    eq(unicode(p), u'Foobar')

def test_recurse_for_nav():
    u = User(username='foo')
    u.save()

    p = Page(
        title='Foobar',
        slug='foo',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p.save()

    p2 = Page(
        parent=p,
        title='child1',
        slug='bar',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p2.save()

    p3 = Page(
        parent=p,
        title='child2',
        slug='baz',
        content='blah',
        created_by=u,
        last_modified_by=u,
        )
    p3.save()

    root = p.get_nav()
    eq(root.page.title, 'Foobar')

    eq(len(root.children), 2)

    child_titles = [c.page.title for c in root.children]
    assert 'child1' in child_titles
    assert 'child2' in child_titles

def test_nav_order():
    u = User(username='foo')
    u.save()

    p = Page(
        title='second',
        slug='foo',
        content='blah',
        created_by=u,
        last_modified_by=u,
        nav_order=10,
        )
    p.save()

    p2 = Page(
        title='first',
        slug='bar',
        content='blah',
        created_by=u,
        last_modified_by=u,
        nav_order=5,
        )
    p2.save()

    pages = Page.objects.all()
    eq(pages[0].title, 'first')
    eq(pages[1].title, 'second')
