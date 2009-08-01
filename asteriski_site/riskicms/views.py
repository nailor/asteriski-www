from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from asteriski_site.riskicms.models import Page

def traverse_for_page(path, manager):
    segments = path.split('/')
    if not segments:
        # Theoretically speaking, this should never happend since root
        # page is caught beforehand
        raise Http404

    page = None
    for segment in segments:
        if not segment:
            # Avoid problems with accidental double slashes, ie. with
            # urls like '/path/to/some//page/', and with the trailing
            # slash
            continue
        if segment.startswith('__'):
            # Don't serve special purpose pages (like __root)
            raise Http404
        try:
            page = manager.get(parent=page, slug=segment)
        except Page.DoesNotExist:
            raise Http404
    return page

def view_page(request):
    if request.user.is_authenticated() and request.user.is_staff:
        manager = Page.objects
    else:
        manager = Page.online_pages

    if request.path == '/':
        # root page
        try:
            page = manager.get(slug='__root')
        except Page.DoesNotExist:
            raise Http404
    else:
        page = traverse_for_page(
            request.path,
            manager=manager,
            )

    return render_to_response(
        page.template,
        {
            'page': page,
            },
        context_instance=RequestContext(request)
        )
