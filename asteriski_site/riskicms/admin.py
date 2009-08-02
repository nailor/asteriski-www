from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from asteriski_site.riskicms.models import Page

class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        is_special = slug.startswith('__')
        if is_special:
            if self.cleaned_data['parent']:
                raise forms.ValidationError(
                    _("Special pages can't have parents")
                    )
        return slug

class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_time'
    list_display = (
        '__unicode__',
        'get_absolute_url',
        'publish_time',
        'created_on',
        'last_modified_on',
        'hidden',
        )
    list_filter = ('hidden',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'slug']
    exclude = [
        'created_by',
        'created_on',
        'last_modified_by',
        'last_modified_on',
        ]
    form = PageAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        obj.save()

    class Media:
        js = (
            '%s/tinymce/jscripts/tiny_mce/tiny_mce_popup.js' % settings.MEDIA_URL,
            '%s/tinymce/jscripts/tiny_mce/tiny_mce.js' % settings.MEDIA_URL,
            '%s/filebrowser/js/TinyMCEAdmin.js' % settings.MEDIA_URL,
            )

admin.site.register(Page, PageAdmin)
