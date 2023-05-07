from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime
from django_mysql.models import ListCharField

class Product(models.Model):
    name = models.CharField(max_length=255)
    video = models.URLField(default='',blank=True)
    paid_proxy = models.URLField(default='',blank=True)
    id_place = models.IntegerField(default=None)
    #dis = models.CharField(max_length=1500)
    dis = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(default='static/images/default.png',upload_to='static/images')
    link = models.URLField(default='',blank=True)
    type = models.CharField(max_length=255,default='Tools')
    hide = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class GroupProduct(models.Model):
    title = models.CharField(max_length=255)
    product = models.ManyToManyField(Product)
    type = models.CharField(max_length=255,default='Tools')
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    product = models.ManyToManyField(Product,default='')
    email_or_username = models.CharField(max_length=255,default='')
    serial = models.CharField(max_length=1000,default='')
    def __str__(self):
        return self.email_or_username
    
    
class RDP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    inovie_rdp = models.IntegerField()
    ip_rdp = models.CharField(max_length=50)
    username_rdp = models.CharField(max_length=100)
    password_rdp = models.CharField(max_length=255)
    
    def __str__(self):
        return self.ip_rdp
class FreeTool(models.Model):
    name = models.CharField(max_length=255)
    dis = models.TextField()
    def __str__(self):
        return self.name
    
class Trending(models.Model):
    name = models.CharField(max_length=255)
    id_place = models.IntegerField()
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class WhoEditSerial(models.Model):
    user = models.CharField(max_length=255,default = '')
    date = models.DateTimeField()
    def __str__(self):
        return self.user

class Basket(models.Model):
    user = models.CharField(max_length=255,default = '')
    items = models.CharField(max_length=1500,default= '')
    def __str__(self):
        return self.user
