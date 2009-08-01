from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from asteriski_site.utils import now

class PageManager(models.Manager):
    def get_query_set(self):
        return super(PageManager, self).get_query_set().filter(
            hidden=False,
            publish_time__lte=now,
            ).exclude(
            expire_time__isnull=False,
            expire_time__lt=now,
            )

class NavNode(object):
    def __init__(self, page):
        self.page = page
        self.highlight = False
        self.children = []

def _child_list(page, child=None):
    result = None
    child_list = []
    if page is not None:
        for c in page.children():
            child_navnode = NavNode(c)
            child_list.append(child_navnode)
            if c == child:
                child_navnode.highlight = True
                result = child_navnode
    return result, child_list

def recurse_for_nav(page, child):
    if page is None:
        root = NavNode(child)
        root.highlight = True
        return root, root
    else:
        navnode, root = recurse_for_nav(page.parent, page)

    result, child_list = _child_list(page, child)
    navnode.children = child_list
    return result, root

class Page(models.Model):
    parent = models.ForeignKey('self', verbose_name=_(u'parent'),
                              null=True, blank=True)
    title = models.CharField(_(u'title'), max_length=500)
    slug = models.SlugField(_(u'URL'))
    content = models.TextField(_(u'content'))
    publish_time = models.DateTimeField(
        _(u'publishing time'),
        help_text=_(u'The day the page is visible on site.'
                    +' You can also set this date to the future'),
        default=now)
    expire_time = models.DateTimeField(
        _(u'Time the page expires'),
        help_text=_(u'Leave this field empty to prevent expiring'),
        null=True,
        blank=True,
        )
    nav_order = models.PositiveIntegerField(_(u'Navigation ordering'),
                                            default=50)
    template = models.CharField(_(u'template'), max_length=500,
                                default='riskicms/default.html')
    created_on = models.DateTimeField(_(u'created on'), default=now)
    created_by = models.ForeignKey(User, verbose_name=_(u'created by'),
                                   related_name='created_by')
    last_modified_by = models.ForeignKey(User, verbose_name=_(u'created by'),
                                         related_name='last_modified_by',)
    last_modified_on = models.DateTimeField(
        _(u'last modified on'),
        default=now
        )
    hidden = models.BooleanField(_(u'page is hidden'), default=False)

    objects = models.Manager()
    online_pages = PageManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug == '__root':
            return '/'
        if self.parent:
            return '%s/%s/' % (self.parent.get_absolute_url().rstrip('/'),
                              self.slug)
        return '/%s/' % self.slug

    def children(self):
        return Page.online_pages.filter(parent=self)

    def get_nav(self):
        navnode, root = recurse_for_nav(self.parent, self)
        dummy, navnode.children = _child_list(self)
        return root

    class Meta:
        unique_together = ('slug', 'parent')
        ordering = ('nav_order', 'title')

