from django.db import models

class Master(models.Model):
    brand=models.CharField("ブランド名",max_length=50)
    hinban=models.CharField("品番",max_length=20)
    hinmei=models.CharField("品名",max_length=100)
    color_no=models.CharField("カラーNo",max_length=10)
    color_name=models.CharField("カラー名",max_length=40)
    size_no=models.CharField("サイズNo",max_length=10)
    size_name=models.CharField("サイズ名",max_length=40)
    jan=models.CharField("JAN",max_length=20)

    def __str__(self):
        return self.jan
