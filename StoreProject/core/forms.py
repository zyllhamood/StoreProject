from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Product,Profile,RDP,Bill
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django_summernote.widgets import SummernoteWidget
class ProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name','style': 'width: 59%;background-color:silver;'}))
    # video = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Video','style': 'width: 59%;background-color:silver;'}))
    # paid_video = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Paid Video','style': 'width: 59%;background-color:silver;'}))
    id_place = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'id_place','style': 'width: 59%;background-color:silver;'}))
    #dis = forms.CharField(widget=SummernoteWidget(attrs={'style': 'background-color:silver;'}))
    dis = forms.CharField(widget=forms.Textarea(attrs={'style': 'background-color:silver;'}))
    price = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Price','style': 'width: 59%;background-color:silver;'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type','style': 'width: 59%;background-color:silver;'}))
    link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Link','style': 'width: 59%;background-color:silver;'}))
    
    
    
    class Meta:
        model = Product
        fields = '__all__'
        # widgets = {
        #     'dis': SummernoteWidget(),
        # }
        
        
class ProductFormPK(forms.ModelForm):
    #dis = forms.CharField(widget=SummernoteWidget())
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    link = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    status = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    id_place = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 59%;background-color:silver;'}))
    #dis = forms.CharField(widget=SummernoteWidget(attrs={'style': 'background-color:silver;'}))
    dis = forms.CharField(widget=forms.Textarea(attrs={'style': 'background-color:silver;'}))
    class Meta:
        model = Product
        fields = '__all__'
        # widgets = {
        #     'dis': SummernoteWidget(),
        # }
    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['user','email_or_username','product','serial']
        
        

class ProfileFormPK(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name','paid_method','type','amount','note']

# class RdpForm(forms.ModelForm):
#     class Meta:
#         model = RDP
#         fields = ['']