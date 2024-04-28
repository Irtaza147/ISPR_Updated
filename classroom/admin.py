from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as AuthUser
from .models import Firmware
from .models import User


# Check if the default User model is registered before unregistering
if admin.site.is_registered(AuthUser):
    admin.site.unregister(AuthUser)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_vendor', 'is_regularuser', 'is_active')
    list_filter = ('is_admin', 'is_vendor', 'is_regularuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_admin', 'is_vendor', 'is_regularuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_admin', 'is_vendor', 'is_regularuser', 'is_active'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)

@admin.register(Firmware)
class Image(admin.ModelAdmin):
    list_display = ['name', 'device_model', 'current_version', 'firmware_file']
