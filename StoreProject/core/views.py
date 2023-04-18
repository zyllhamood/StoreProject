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
from .models import Product,GroupProduct,Profile,RDP,FreeTool,Trending
from .serializers import ProductSerializer,ProfileSerializer,UserSerializer
from .forms import ProductForm,ProductFormPK,ProfileFormPK,ProfileForm,EditProfile
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
import re
from django.http import JsonResponse
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
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
def tools(request):
    model = Product.objects.all().order_by('id_place')
    groups = GroupProduct.objects.all()
    content = {"products":model,"groups": groups}
    return render(request,'tools.html',content)

def info(request,name=None):
    model = Product.objects.get(name=name)
    # client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    # product = {
    #     'name': model.name,
    #     'local_price':{
    #         'amount': model.price,
    #         'currency': 'USD'
    #         } ,
    #     'pricing_type': 'fixed_price',
    # }
    # charge = client.charge.create(**product)
    content = {
        "id": model,
        #"charge": charge,
        }
    return render(request,'info-product.html',content)



class NewProduct(generic.edit.CreateView):
    model = Product
    form_class = ProductForm
    #fields = '__all__'
    template_name = 'new_product.html'
    success_url = '/'
    
class EditProduct(generic.edit.UpdateView):

    model = Product
    form_class = ProductFormPK
    #fields = '__all__'
    template_name = 'edit-product.html'
    success_url = '/tools/'
    
    
class DeleteProduct(generic.edit.DeleteView):

    model = Product
    #form_class = ProductFormPK
    #fields = '__all__'
    template_name = 'delete-product.html'
    success_url = '/tools/'
    def post(request,pk):
        Product.objects.filter(pk=pk).delete()
        return redirect('/tools/')
    
def delete_product(request,pk):
    if request.method == "GET":
        return render(request,'delete-product.html')
    elif request.method == "POST":
        Product.objects.filter(pk=pk).delete()
        return redirect('/tools/')

def error_404_view(request,exception):
    return render(request,'404.html')


def groups_view(request,title):
    model = GroupProduct.objects.get(title=title)
    groups = GroupProduct.objects.all()
    #print(model.product.all())
    return render(request,'groups.html',{"content": model.product.all().order_by('id_place'),"groups": groups})

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

@ratelimit(key='ip', rate='5/m')
def login_page(request):
    ip = request.META['REMOTE_ADDR']
    was_limited = getattr(request, 'limited', False)
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
    success_url = '/show-users/'
    
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


# class ProfileCreateView(generic.CreateView):
#     template_name = 'new-user.html'
#     model = User
#     fields = '__all__'
#     #form_class = ProfileForm
#     #success_url = 'add-user/'

# class ProfileEditView(generic.UpdateView):
#     template_name = 'new-user.html'
#     model = Profile
#     form_class = ProfileForm
    

def homeFreeTools(request):
    model = FreeTool.objects.all()
    #groups = GroupProduct.objects.all()
    content = {"model":model}
    return render(request,'free-tools.html',content)
def call_request(request):
    if request.method == "GET":
        return render(request,'free/call-request.html')
    elif request.method == "POST":
        method = request.POST['method']
        url = request.POST['url']
        headers = request.POST['headers']
        data = request.POST['data']
        #content = {"method": request.POST['method'],"url": request.POST['url'],"headers": request.POST['headers'],"data": request.POST['data']}
        head = {}
        headers = headers.splitlines()
        for item in headers:
            txt = item.split(': ')
            head[txt[0]] = txt[1]
        if (method == "POST"):
            try:
                resp = requests.post(url,headers=head,data=data)
            except Exception as e:
                resp = ''
                if 'latin-1' in str(e):
                    resp = requests.post(url,headers=head,data=data.encode('utf-8'))
        else:
            resp = requests.get(url,headers=head)
        print(resp.text)
        content = {"text": resp.text,"status_code": resp.status_code,"cookies": resp.cookies}
        return render(request,'free/show-response.html',content)
def made_request(request):
    if request.method == "GET":
        return render(request,'free/request-function.html')
    elif request.method == "POST":
        method = request.POST['method']
        print(method)
        type = request.POST['type']
        url = request.POST['url']
        headers = request.POST['headers']
        data = request.POST['data']
        if type == "Python":
            head = {}
            headers = headers.splitlines()
            for item in headers:
                txt = item.split(': ')
                if txt[0] == "Connection" or txt[0] == "Content-Length" or txt[0] == "Accept-Language":
                    continue
                head[txt[0]] = txt[1]
            content = {"type": type,"method": method,"url": url, "headers": head, "data": data}
        else:
            head = {}
            headers = headers.splitlines()
            useragent = ''
            for item in headers:
                txt = item.split(': ')
                if txt[0] == "Connection" or txt[0] == "Content-Length" or txt[0] == "Accept-Language":
                    continue
                if txt[0] == "User-Agent" or txt[0] == "user-agent":
                    useragent = txt[1]
                    continue
                head[txt[0]] = txt[1]
            
            h = ""
            for item in head:
                if item == "User-Agent" or item == "user-agent":
                    continue
                h+= f'httpRequest.AddHeader("{item}", "{head[item]}");'
            hh = h.split('");')
            content = {"type": type,"method": method,"url": url, "headers": hh, "data": data,"useragent":useragent}
        return render(request,'free/resp-function-request.html',content)

@ratelimit(key='ip', rate='20/h')
def get_session(request):
    if request.method == "GET":
        return render(request,'free/get-session.html',{"resp":"57770835548%3AEce3stFv2Oul5q%3A16%3AAYcF1MONzV_VuzLU9CD6kSm0X8ReomStLQBoPsZEkQ"})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        url = 'https://i.instagram.com/api/v1/accounts/login/'
        headers = {'X-IG-Connection-Speed': '308kbps', 'Accept': '*/*', 'X-IG-Connection-Type': 'WiFi', 'X-IG-App-ID': '124024574287414', 'Accept-Encoding': 'br, gzip, deflate', 'Accept-Language': 'ar-SA;q=1', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-IG-ABR-Connection-Speed-KBPS': '0', 'Content-Length': '414', 'User-Agent': 'Instagram 50.0.0.52.188 (iPhone7,2; iOS 12_5_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; gamut=normal; 750x1334) AppleWebKit/420+', 'Connection': 'keep-alive', 'X-IG-Capabilities': '36r/dw=='}
        data = 'signed_body=89148f827c1efffe8e4c0bbf4a81f5e60b32fd3ab4bdef0e354736f1d3e09934.{"reg_login":"0","password":"'+password+'","device_id":"A6ECB176-7695-4893-9185-A478D3B10BFD","username":"'+username+'","adid":"ED063999-948C-4B83-A80F-D412E3DB21DA","login_attempt_count":"0","phone_id":"A6ECB176-7695-4893-9185-A478D3B10BFD"}&ig_sig_key_version=5'
        resp = requests.post(url,headers=headers,data=data)
        if 'sessionid' in resp.cookies:
            session = re.findall(r'sessionid=(.*?) for', str(resp.cookies))[0]
            return render(request,'free/resp-session.html',{"resp":session})
        return render(request,'free/resp-session.html',{"resp":resp.text})
        
def index(request):
    model = Trending.objects.all().order_by('id_place')
    content = {"model": model}
    return render(request,'index.html',content)

def show_products(request):
    model = Product.objects.all().order_by('id_place')
    groups = GroupProduct.objects.all()
    content = {"products":model,"groups": groups}
    return render(request,'products.html',content)

def reset_instagram(request):
    if request.method == "GET":
        return render(request,'free/reset-instagram.html')
    elif request.method == "POST":
        email_or_username = request.POST['email_or_username']
        url = 'https://www.instagram.com/accounts/account_recovery_send_ajax/'
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": "missing"
        }
        data = f'email_or_username={email_or_username}&recaptcha_challenge_field=&flow=fxcal&app_id=&source_account_id='
        resp = requests.post(url,headers=headers,data=data).json()['message']
        return render(request,'free/resp-reset-instagram.html',{"resp": resp})


# class ShowUsers(generic.ListView):
#     template_name = 'show-users.html'
#     model = User
#     fields = ['username']
#     #form_class = ProfileForm
#     #success_url = 'add-user/'

def show_users(request):
    if request.method == "GET":
        model = User.objects.all().order_by('-date_joined')
        model2 = Profile.objects.all()
        content = {"userx":model,"profile":model2}
        return render(request,'show-users.html',content)
    elif request.method == "POST":
        word = request.POST["word"]
        model = User.objects.filter(username__contains=word).order_by('-date_joined')
        model2 = Profile.objects.all()
        content = {"userx":model,"profile":model2}
        return render(request,'show-users.html',content)

def edit_user(request,user):
    model = Profile.objects.get(email_or_username=user)
    content = {"user": model}
    return render(request,'edit-user.html',content)


class EditUser(generic.UpdateView):
    model = Profile
    form = EditProfile()
    #fields = ['serial']
    fields = '__all__'
    template_name = "edit-user.html"
    success_url = '/show-users/'

class CreateProfile(generic.CreateView):
    model = Profile
    form = EditProfile()
    #fields = ['serial']
    fields = '__all__'
    template_name = "edit-user.html"
    success_url = '/show-users/'
    