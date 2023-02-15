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
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm,ProductFormPK
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
    content = {"products":model}
    return render(request,'home.html',content)

def info(request,pk=None):
    model = Product.objects.get(pk=pk)
    content = {"id":model}
        
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