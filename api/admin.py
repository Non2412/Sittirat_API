from django.contrib import admin
from .models import Placeholder


@admin.register(Placeholder)
class PlaceholderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
