import tagging

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from asteriski_site.utils import now

INFO = 1
PARTY = 2
STUDIES = 3
FILE = 4
EVENTS = 5
RECRUITING = 6

CATEGORY_CHOICES = (
    (INFO, _('INFO')),
    (PARTY, _('PARTY')),
    (STUDIES, _('STUDIES')),
    (FILE, _('FILE')),
    (EVENTS, _('EVENTS')),
    (RECRUITING, _('RECRUITING')),
    )

class Message(models.Model):
    """Model representing single Riski-info message"""

    title = models.CharField(_('title'), max_length=120)
    category = models.IntegerField(_('category'), choices=CATEGORY_CHOICES)
    content = models.TextField(_('content'))
    creator = models.ForeignKey(User, related_name='created_messages',
                                verbose_name=_('creator'))
    created_on = models.DateTimeField(default=now)
    last_modifier = models.ForeignKey(User, related_name='modified_messages',
                                      null=True,
                                      verbose_name=_('last modified by'))
    last_modified_on = models.DateTimeField(_('last modified on'), null=True)

    def __unicode__(self):
        return u'[%s] %s' % (
            self.get_category_display(),
            self.title,
            )

    def save(self):
        if self.id:
            self.last_modified_on = now()
        super(Message, self).save()

tagging.register(Message)
