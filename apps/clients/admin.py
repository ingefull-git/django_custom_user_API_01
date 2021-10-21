from django.contrib import admin
from apps.clients.models import Client


class CustomClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'email', 'status', 'created', 'updated')
    list_display_links = ('id', 'lname')
    ordering = ('-created', 'lname')
    search_fields = ('id', 'fname', 'lname', 'email', 'status')
    list_filter = ('id', 'fname', 'lname', 'email', 'status', 'created', 'updated')
    readonly_fields = ('created', 'updated')


admin.site.register(Client, CustomClientAdmin)

