from django.contrib import admin
from .models import CustomUserModel

# Register your models here.


@admin.register(CustomUserModel)
class CustomUser(admin.ModelAdmin):
    list_display = ("email", "username", "is_admin")
    ordering = ("-date_joined",)
