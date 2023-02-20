from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    id_place = models.IntegerField(default=None)
    #dis = models.CharField(max_length=1500)
    dis = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(default='static/images/default.png',upload_to='static/images')
    def __str__(self):
        return self.name
    
class GroupProduct(models.Model):
    title = models.CharField(max_length=255)
    product = models.ManyToManyField(Product)
    def __str__(self):
        return self.title