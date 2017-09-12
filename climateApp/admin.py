from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, City

class CityAdmin(admin.ModelAdmin):
    list_display = ('cityId', 'cityName')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',     'displayName', 'mobile', 'photo')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(City, CityAdmin)