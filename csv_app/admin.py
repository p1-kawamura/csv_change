from django.contrib import admin
from .models import Master
from django.contrib.admin import ModelAdmin

class Mas(ModelAdmin):
    model=Master
    list_display=["id","jan","hinban","kataban",]
    search_fields = ['jan']

admin.site.register(Master,Mas)
