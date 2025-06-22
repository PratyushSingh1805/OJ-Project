from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

# Step 1: Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Step 2: Extend the existing User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Step 3: Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
