from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin



class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fields = ['age', 'national_code']
    
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff']
    inlines = [UserProfileInline]

    search_fields = ['id', 'username']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    fields = ['user', 'age', 'national_code']
