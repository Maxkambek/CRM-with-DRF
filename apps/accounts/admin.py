from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'date_login']


admin.site.register(Account, AccountAdmin)
