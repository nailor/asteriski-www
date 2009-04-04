from django.contrib import admin
from asteriski_site.riski_info.models import Message

class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    fieldsets = (
        (None, {
                'fields': ('title', 'category', 'content')
                }),
        )

    def save_model(self, request, obj, form, change):
        if obj.id:
            obj.last_modifier = request.user
        else:
            obj.creator = request.user
        obj.save()

admin.site.register(Message, MessageAdmin)
