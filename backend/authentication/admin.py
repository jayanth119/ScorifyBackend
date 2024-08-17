from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomAdmin(UserAdmin):
    model = CustomUser
    
    # Remove 'id' from 'fieldsets'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Removed 'id'
        ("Permissions", {"fields": ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    # Remove 'id' from 'add_fieldsets'
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ("email", "password", "password2")
            }
        ),
    )
    
    # You can keep 'id' in list_display and search_fields
    list_display = ("email", "id", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "id")
    ordering = ("email",)
    
    # Exclude fields that are not used
    exclude = ('first_name', 'last_name', 'username')

admin.site.register(CustomUser, CustomAdmin)
