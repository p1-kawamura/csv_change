from django.forms import ModelForm
from .models import Master

class Masterform(ModelForm):
    class Meta:
        model=Master
        fields=[
            "brand",
            "hinban",
            "hinmei",
            "color_no",
            "color_name",
            "size_no",
            "size_name",
            "jan",]