from django.db import models

kata=[
    ("1","01"),
    ("2","02"),
    ("3","03"),
    ("4","04"),
    ("7","07"),
    ]
class Master(models.Model):
    jan=models.CharField("JAN",max_length=20)
    hinban=models.CharField("品番",max_length=10)
    kataban=models.CharField("型番",choices=kata,max_length=10)
    
    def __str__(self):
        return self.jan
