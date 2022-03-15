from django.urls import path
from .views import index,master,csv_import,csv_export,master_kanri,master2

urlpatterns = [
    path('', index, name="index"),
    path('master/', master, name="master"),
    path('csv_import/', csv_import, name="csv_import"),
    path('csv_export/', csv_export, name="csv_export"),
    path('master_kanri/', master_kanri, name="master_kanri"),
    path('master2/', master2, name="master2"),
]
