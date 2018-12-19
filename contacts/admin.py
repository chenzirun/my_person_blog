from django.contrib import admin
from .models import Contacts
# Register your models here.

class ContactsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']

admin.site.register(Contacts, ContactsAdmin)