from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'nickname', 'email', 'balance', 'is_premium')
    search_fields = ('username', 'nickname', 'email')
    ordering = ('-date_joined',)
    list_filter = ('is_staff', 'is_active')

