from django.contrib import admin
from .models import Master,Trade_hinban,Trade_kyoten
from django.contrib.admin import ModelAdmin

class Mas(ModelAdmin):
    model=Master
    list_display=["id","jan","hinban","kataban",]
    search_fields = ['jan']

class Tra_hin(ModelAdmin):
    model=Trade_hinban
    list_display=["id","jan","hinban"]
    search_fileds=["jan"]

class Tra_kyo(ModelAdmin):
    model=Trade_kyoten
    list_display=["id","name","ninushi_name"]
    search_fileds=["name"]


admin.site.register(Master,Mas)
admin.site.register(Trade_hinban,Tra_hin)
admin.site.register(Trade_kyoten,Tra_kyo)
