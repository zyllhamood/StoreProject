from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import throttle_classes,action,permission_classes
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from .models import Product,GroupProduct
from .serializers import ProductSerializer
from .forms import ProductForm,ProductFormPK
from decimal import Decimal
from StoreProject import settings
from coinbase_commerce.client import Client
import logging
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import re
class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]
class ProductViewPK(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]
    
def home(request):
    model = Product.objects.all().order_by('id_place')
    groups = GroupProduct.objects.all()
    content = {"products":model,"groups": groups}
    return render(request,'home.html',content)

def info(request,pk=None):
    model = Product.objects.get(pk=pk)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    product = {
        'name': model.name,
        'local_price':{
            'amount': str(model.price),
            'currency': 'USD'
            } ,
        'pricing_type': 'fixed_price',
        
        
    }
    charge = client.charge.create(**product)
    amount = 0.20
    coupun = model.price * Decimal(amount)
    coupun = model.price - coupun
    coupun = '{:.2f}'.format(coupun)
    content = {
        "id": model,
        "coupun": coupun,
        "charge": charge
        }
    
    return render(request,'info-product.html',content)

class NewProduct(CreateView):
    model = Product
    form = ProductForm()
    fields = '__all__'
    template_name = 'new_product.html'
    success_url = '/'
    
class EditProduct(UpdateView):
    
    model = Product
    form = ProductFormPK()
    fields = '__all__'
    template_name = 'edit-product.html'
    success_url = '/'

def error_404_view(request,exception):
    return render(request,'404.html')

def groups_view(request,title):
    model = GroupProduct.objects.get(title=title)
    group = GroupProduct.objects.all()
    #print(model.product.all())
    return render(request,'groups.html',{"content": model.product.all().order_by('id_place'),"group": group})

def payment_view(request,pk):
    model = Product.objects.get(pk=pk)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    product = {
        'name': model.name,
        'local_price':{
            'amount': str(model.price),
            'currency': 'USD'
            } ,
        'pricing_type': 'fixed_price',
        
        
    }
    charge = client.charge.create(**product)
    amount = 0.20
    coupun = model.price * Decimal(amount)
    coupun = model.price - coupun
    #print(float(coupun))
    coupun = '{:.2f}'.format(coupun)
    content = {
        "form": model,
        "coupun": coupun,
        #"charge": charge
        }
    return render(request,'payment-method.html',content)