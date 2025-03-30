from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")  # Show these fields in admin panel
    list_filter = ("role", "is_staff", "is_active")  # Add filters
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email", "username")  # Enable search
    ordering = ("email",)  # Order by email

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
