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


class Trade_hinban(models.Model):
    jan=models.CharField("JAN",max_length=20)
    hinban=models.CharField("品番",max_length=20)

    def __str__(self):
        return self.jan


class Trade_kyoten(models.Model):
    name=models.CharField("名称",max_length=50)
    yubin=models.CharField("郵便番号",max_length=7)
    pref=models.CharField("都道府県",max_length=4)
    address1=models.CharField("住所1",max_length=16)
    address2=models.CharField("住所2",max_length=28)
    company=models.CharField("会社名",max_length=16,blank=True)
    sei=models.CharField("姓",max_length=5)
    mei=models.CharField("名",max_length=5,blank=True)
    tel=models.CharField("電話番号",max_length=11)
    ninushi_name=models.CharField("荷主名",max_length=20)
    ninushi_tel=models.CharField("荷主電話",max_length=11)

    def __str__(self):
        return self.name

