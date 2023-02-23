from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import throttle_classes,action,permission_classes
#from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from .models import Product,GroupProduct,Profile
from .serializers import ProductSerializer,ProfileSerializer,UserSerializer
from .forms import ProductForm,ProductFormPK,ProfileFormPK
from decimal import Decimal
from StoreProject import settings
from coinbase_commerce.client import Client
from django.contrib.auth.forms import UserCreationForm
#from django.views.generic import CreateView
from django.contrib.auth import authenticate , login , logout
from django.views import generic
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]
    
class ProfileSerilaizerView(APIView):
    queryset = Profile.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    # fields = ['email_or_username','product','serial']
    throttle_classes = [AnonRateThrottle]
    def get(self,request):
        model = Profile.objects.all()
        serializer = ProfileSerializer(model,many=True)
        return Response(serializer.data)
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

    content = {
        "id": model,
        "charge": charge
        }

    return render(request,'info-product.html',content)

class NewProduct(generic.edit.CreateView):
    model = Product
    form = ProductForm()
    fields = '__all__'
    template_name = 'new_product.html'
    success_url = '/'
    
class EditProduct(generic.edit.UpdateView):

    model = Product
    form = ProductFormPK()
    fields = '__all__'
    template_name = 'edit-product.html'
    success_url = '/'


def error_404_view(request,exception):
    return render(request,'404.html')

def paypal_view(request,pk):
    model = Product.objects.get(pk=pk)
    return render(request,'pay.html',{"product": model})

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
    content = {
        "form": model,
        "charge": charge
        }
    return render(request,'payment-method.html',content)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == "GET":
            return render(request,'registration/login.html')
        elif request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('profile')
            else:
                print('wrong username or password')
                return redirect('login')
def logout_user(request):
    logout(request)
    return redirect('login')

class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = UserCreationForm
    success_url = 'login/'
    
#@method_decorator(login_required(login_url='login'),name='dispatch')
class ProfileView(ListView):
    model = User
    template_name = "profile.html"
    
    
    
def profile_view(request):
    model = Profile
    
    return render(request,'profile.html',{"item": model})
    
    
class EditProfileView(generic.UpdateView):
    model = Profile
    form = ProfileFormPK()
    fields = ['serial']
    template_name = "edit-profile.html"
    success_url = '/profile/'
