from django.contrib import admin
from .models import Master
from django.contrib.admin import ModelAdmin

class Mas(ModelAdmin):
    model=Master
    list_display=["brand","hinban","hinmei","color_no","color_name","size_no","size_name","jan"]

admin.site.register(Master,Mas)
