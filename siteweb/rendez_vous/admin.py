from django.contrib import admin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin for User model"""
list_display = ('username', 'email', 'is_staff', 'is_superuser')
fields = ('username', 'nom', 'adresse', 'email', 'numero_de_telephone', 'password', 'is_active', 'is_staff', 'is_superuser')

