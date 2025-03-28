from django.contrib import admin
from .models import City

# Register your models here
# You can add cities in the admin panel too and it should work.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'temperature', 'conditions')
    search_fields = ('name', 'conditions')
    list_filter = ('conditions',)
