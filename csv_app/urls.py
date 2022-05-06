from django.urls import path
from .views import index,csv_import,csv_export,master_kanri,master,master2,master3,trade_hinban,trade_kyoten,trade_hinban_ajax,trade_hinban2_ajax

urlpatterns = [
    path('', index, name="index"),
    path('master/', master, name="master"),
    path('csv_import/', csv_import, name="csv_import"),
    path('csv_export/', csv_export, name="csv_export"),
    path('master_kanri/', master_kanri, name="master_kanri"),
    path('master2/', master2, name="master2"),
    path('master3/', master3, name="master3"),
    path('trade_hinban/', trade_hinban, name="trade_hinban"),
    path('trade_kyoten/', trade_kyoten, name="trade_kyoten"),
    path('trade_hinban_ajax/', trade_hinban_ajax, name="trade_hinban_ajax"),
    path('trade_hinban2_ajax/', trade_hinban2_ajax, name="trade_hinban2_ajax"),
]
