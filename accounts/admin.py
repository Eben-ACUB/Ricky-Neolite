from django.contrib import admin

from .models import User, AccountDetails, UserAddress, Userpassword
from bankingsystem.admin_actions import export_as_csv



class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username' , 'balance', 'account_status')



    def account_status(self, obj):
        if obj.account:
            return 'Active'
        return 'Inactive'
    account_status.short_description = 'Account Status'


admin.site.register(User, UserAdmin)
admin.site.register(Userpassword)


@admin.register(AccountDetails)
class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'account_no', 'balance']
    search_fields = ['user__username', 'account_no']



    def username(self, obj):
        return obj.user.username

    username.short_description = 'Username'



admin.site.add_action(export_as_csv, name='export_selected')
