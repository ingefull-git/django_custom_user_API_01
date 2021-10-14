from django.contrib import admin
from apps.clients.models import Client


class CustomClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'created', 'updated')
    list_display_links = ('id', 'lname')
    ordering = ('-created', 'lname')
    search_fields = ('id', 'fname', 'lname')
    list_filter = ('id', 'fname', 'lname', 'created', 'updated')
    readonly_fields = ('created', 'updated')


admin.site.register(Client, CustomClientAdmin)

