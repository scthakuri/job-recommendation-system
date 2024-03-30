from django.contrib import admin
from userauth.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # list_display = ['username', 'email', 'last_login']
    # exclude = ('password',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('skills', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')

admin.site.register(User, UserAdmin)