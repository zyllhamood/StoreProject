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
from .models import Product,GroupProduct,Profile,RDP
from .serializers import ProductSerializer,ProfileSerializer,UserSerializer
from .forms import ProductForm,ProductFormPK,ProfileFormPK,ProfileForm
from decimal import Decimal
from StoreProject import settings
from coinbase_commerce.client import Client
from django.contrib.auth.forms import UserCreationForm
#from django.views.generic import CreateView
from django.contrib.auth import authenticate , login , logout
from django.views import generic
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
import requests
from django.http import HttpResponse

def get_coupun(price):
    amount = 0.20
    coupun = price * Decimal(amount)
    coupun = price - coupun
    coupun = '{:.2f}'.format(coupun)
    return coupun
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
            'amount': model.price,
            'currency': 'USD'
            } ,
        'pricing_type': 'fixed_price',
    }
    charge = client.charge.create(**product)
    content = {
        "id": model,
        "charge": charge,
        }
    return render(request,'info-product.html',content)

def info_coupun(request,pk=None):
    model = Product.objects.get(pk=pk)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    coupun = get_coupun(model.price)
    print(type(coupun))
    product = {
        'name': model.name,
        'local_price':{
            'amount': str(coupun),
            'currency': 'USD'
            } ,
        'pricing_type': 'fixed_price',
    }
    charge = client.charge.create(**product)

    content = {
        "id": model,
        "charge": charge,
        "coupun": coupun,
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
                return redirect('loginurl')
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
    #send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text
    fields = ['serial']
    template_name = "edit-profile.html"
    success_url = '/profile/'
    
        
    # def get(request,pk):
    #     send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text
    # def post(request,pk):
    #     send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text
        
    

def rdp_control(request):
    model = RDP.objects.get(user=request.user)
    #print(request.user.username)
    #print(model.ip_rdp)
    
    
    
    
    return render(request,'rdp-control.html',{"model": model})

def action_rdp(request,action):
    model = RDP.objects.get(user=request.user)
    print(model.inovie_rdp)
    url = f'https://hostdzire.com/billing/index.php?avmAction={action}&avmServiceId={str(model.inovie_rdp)}'
    Headers = {
        "Host": "hostdzire.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        #"Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "hostdzire.com",
        "Connection": "keep-alive",
        "Cookie": "WHMCSuUM4sUcCcJns=cf2f997ccb1b9a09d56681bb817b20c9",
    }
    resp = requests.get(url, headers=Headers).text
    if str(model.ip_rdp) in resp:
        #return redirect('rdp')
        return render(request,'rdp-control.html',{"model": model,"status": "true"})
    return render(request,'rdp-control.html',{"model": model,"status": "false"})


class ProfileCreateView(generic.CreateView):
    template_name = 'new-user.html'
    model = User
    fields = '__all__'
    #form_class = ProfileForm
    #success_url = 'add-user/'

class ProfileEditView(generic.UpdateView):
    template_name = 'new-user.html'
    model = Profile
    form_class = ProfileForm
    
