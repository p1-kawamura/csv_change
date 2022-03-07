from django.urls import path
from .views import index,master,csv_import,csv_export

urlpatterns = [
    path('', index, name="index"),
    path('master/', master, name="master"),
    path('csv_import/', csv_import, name="csv_import"),
    path('csv_export/', csv_export, name="csv_export"),
]
