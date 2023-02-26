from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Product,Profile,RDP
from django.contrib.auth.models import User
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
    
class ProfileFormPK(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('serial',)
    
# class RdpForm(forms.ModelForm):
#     class Meta:
#         model = RDP
#         fields = ['']