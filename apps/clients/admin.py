from django.contrib import admin
from apps.clients.models import Client, Invoice



class CustomClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'psid', 'fname', 'lname', 'email', 'status', 'created', 'updated')
    list_display_links = ('id', 'psid', 'lname')
    ordering = ('-created', 'lname')
    search_fields = ('id', 'psid', 'fname', 'lname', 'email', 'status')
    list_filter = ('id', 'psid', 'fname', 'lname', 'email', 'status', 'created', 'updated')
    readonly_fields = ('created', 'updated')


admin.site.register(Client, CustomClientAdmin)
admin.site.register(Invoice)

