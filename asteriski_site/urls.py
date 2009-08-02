from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from asteriski_site.riskicms.views import view_page

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'.*/$', view_page),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}
         ),
    )
