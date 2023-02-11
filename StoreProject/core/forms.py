from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Product
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django_summernote.widgets import SummernoteWidget
class ProductForm(forms.ModelForm):
    dis = forms.CharField(widget=SummernoteWidget)
    class Meta:
        model = Product
        fields = ['name','id_place','dis','price','image']
        
        
class ProductFormPK(forms.ModelForm):
    dis = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Product
        fields = ('name','id_place','dis','price','image')
    
    