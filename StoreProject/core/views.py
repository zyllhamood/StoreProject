from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import throttle_classes, action, permission_classes
# from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from .models import Product, GroupProduct, Profile, RDP, FreeTool, Trending,WhoEditSerial,Basket,Serial,ProductsPaid
from .serializers import ProductSerializer, ProfileSerializer, UserSerializer
from .forms import ProductForm, ProductFormPK, ProfileFormPK, ProfileForm, EditProfile
from decimal import Decimal
from StoreProject import settings
from coinbase_commerce.client import Client
from django.contrib.auth.forms import UserCreationForm
# from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
import requests
import re
from django.http import JsonResponse
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from collections import OrderedDict
import json
from django.shortcuts import redirect
import datetime
from django.contrib.admin.views.decorators import user_passes_test

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
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    # fields = ['email_or_username','product','serial']
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        model = Profile.objects.all()
        serializer = ProfileSerializer(model, many=True)
        return Response(serializer.data)


class ProductViewPK(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]


def tools(request):
    model = Product.objects.all().order_by('id_place')
    groups = GroupProduct.objects.all()
    content = {"products": model, "groups": groups}
    return render(request, 'tools.html', content)


def info(request, name=None):
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
        # "charge": charge,
    }
    return render(request, 'info-product.html', content)


class NewProduct(generic.edit.CreateView):
    model = Product
    form_class = ProductForm
    # fields = '__all__'
    template_name = 'new_product.html'
    success_url = '/'


class EditProduct(generic.edit.UpdateView):

    model = Product
    form_class = ProductFormPK
    # fields = '__all__'
    template_name = 'edit-product.html'
    success_url = '/tools/'


class DeleteProduct(generic.edit.DeleteView):

    model = Product
    # form_class = ProductFormPK
    # fields = '__all__'
    template_name = 'delete-product.html'
    success_url = '/tools/'

    def post(request, pk):
        Product.objects.filter(pk=pk).delete()
        return redirect('/tools/')


def delete_product(request, pk):
    if request.method == "GET":
        return render(request, 'delete-product.html')
    elif request.method == "POST":
        Product.objects.filter(pk=pk).delete()
        return redirect('/tools/')


def error_404_view(request, exception):
    return render(request, '404.html')


def groups_view(request, title):
    model = GroupProduct.objects.get(title=title)
    groups = GroupProduct.objects.all()
    # print(model.product.all())
    return render(request, 'groups.html', {"content": model.product.all().order_by('id_place'), "groups": groups})


def payment_view(request, pk):
    model = Product.objects.get(pk=pk)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    product = {
        'name': model.name,
        'local_price': {
            'amount': str(model.price),
            'currency': 'USD'
        },
        'pricing_type': 'fixed_price',


    }
    charge = client.charge.create(**product)
    content = {
        "form": model,
        "charge": charge
    }
    return render(request, 'payment-method.html', content)


@ratelimit(key='ip', rate='5/m')
def login_page(request):
    ip = request.META['REMOTE_ADDR']
    was_limited = getattr(request, 'limited', False)
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == "GET":
            return render(request, 'registration/login.html')
        elif request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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

# @method_decorator(login_required(login_url='login'),name='dispatch')


class ProfileView(ListView):
    model = User
    template_name = "profile.html"


def profile_view(request):
    model = Profile
    return render(request, 'profile.html', {"item": model})


class EditProfileView(generic.UpdateView):
    model = Profile
    form = ProfileFormPK()
    # send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text
    fields = ['serial']
    template_name = "edit-profile.html"
    success_url = '/profile/'



#@ratelimit(key='ip', rate='3/h')
def edit_profile(request, pk):
    obj = get_object_or_404(Profile, pk=pk)
    print(obj)
    if request.method == 'POST':
        serials = Serial.objects.all()
        myserial = request.POST['serial']
        if str(myserial) in str(serials):
            return HttpResponse("Serial is edited before. You cannot repeat same serial")
        form = ProfileFormPK(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            who_edit = WhoEditSerial.objects.create(user=request.user.username,date=datetime.datetime.now())
            who_edit.save()
            add_serial = Serial.objects.create(user=request.user.username,serial=request.POST['serial'])
            print(request.POST['serial'])
            add_serial.save()
            return redirect('profile')
    else:
        form = ProfileFormPK(instance=obj)
    return render(request, 'edit-profile.html', {'form': form})


def add_data(request, pk):
    if request.method == 'POST':
        form = ProfileFormPK(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileFormPK()
    return render(request, 'edit-profile.html', {'form': form})

    # def get(request,pk):
    #     send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text
    # def post(request,pk):
    #     send = requests.get(f'https://api.telegram.org/bot6157529177:AAF5OSVN2n1pUksGAq1xXS61v0k0ucOZrVM/sendMessage?chat_id=1282345978&text=xx').text


def rdp_control(request):
    model = RDP.objects.get(user=request.user)
    # print(request.user.username)
    # print(model.ip_rdp)

    return render(request, 'rdp-control.html', {"model": model})


def action_rdp(request, action):
    model = RDP.objects.get(user=request.user)
    print(model.inovie_rdp)
    url = f'https://hostdzire.com/billing/index.php?avmAction={action}&avmServiceId={str(model.inovie_rdp)}'
    Headers = {
        "Host": "hostdzire.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        # "Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "hostdzire.com",
        "Connection": "keep-alive",
        "Cookie": "WHMCSuUM4sUcCcJns=cf2f997ccb1b9a09d56681bb817b20c9",
    }
    resp = requests.get(url, headers=Headers).text
    if str(model.ip_rdp) in resp:
        # return redirect('rdp')
        return render(request, 'rdp-control.html', {"model": model, "status": "true"})
    return render(request, 'rdp-control.html', {"model": model, "status": "false"})


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
    # groups = GroupProduct.objects.all()
    content = {"model": model}
    return render(request, 'free-tools.html', content)


def call_request(request):
    if request.method == "GET":
        return render(request, 'free/call-request.html')
    elif request.method == "POST":
        method = request.POST['method']
        url = request.POST['url']
        headers = request.POST['headers']
        data = request.POST['data']
        # content = {"method": request.POST['method'],"url": request.POST['url'],"headers": request.POST['headers'],"data": request.POST['data']}
        head = {}
        headers = headers.splitlines()
        for item in headers:
            txt = item.split(': ')
            head[txt[0]] = txt[1]
        if (method == "POST"):
            try:
                resp = requests.post(url, headers=head, data=data)
            except Exception as e:
                resp = ''
                if 'latin-1' in str(e):
                    resp = requests.post(
                        url, headers=head, data=data.encode('utf-8'))
        else:
            resp = requests.get(url, headers=head)
        print(resp.text)
        content = {"text": resp.text,
                   "status_code": resp.status_code, "cookies": resp.cookies}
        return render(request, 'free/show-response.html', content)


def made_request(request):
    if request.method == "GET":
        return render(request, 'free/request-function.html')
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
            content = {"type": type, "method": method,
                       "url": url, "headers": head, "data": data}
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
                h += f'httpRequest.AddHeader("{item}", "{head[item]}");'
            hh = h.split('");')
            content = {"type": type, "method": method, "url": url,
                       "headers": hh, "data": data, "useragent": useragent}
        return render(request, 'free/resp-function-request.html', content)


@ratelimit(key='ip', rate='20/h')
def get_session(request):
    if request.method == "GET":
        return render(request, 'free/get-session.html', {"resp": "57770835548%3AEce3stFv2Oul5q%3A16%3AAYcF1MONzV_VuzLU9CD6kSm0X8ReomStLQBoPsZEkQ"})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        url = 'https://i.instagram.com/api/v1/accounts/login/'
        headers = {'X-IG-Connection-Speed': '308kbps', 'Accept': '*/*', 'X-IG-Connection-Type': 'WiFi', 'X-IG-App-ID': '124024574287414', 'Accept-Encoding': 'br, gzip, deflate', 'Accept-Language': 'ar-SA;q=1', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'X-IG-ABR-Connection-Speed-KBPS': '0', 'Content-Length': '414', 'User-Agent': 'Instagram 50.0.0.52.188 (iPhone7,2; iOS 12_5_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; gamut=normal; 750x1334) AppleWebKit/420+', 'Connection': 'keep-alive', 'X-IG-Capabilities': '36r/dw=='}
        data = 'signed_body=89148f827c1efffe8e4c0bbf4a81f5e60b32fd3ab4bdef0e354736f1d3e09934.{"reg_login":"0","password":"'+password+'","device_id":"A6ECB176-7695-4893-9185-A478D3B10BFD","username":"' + \
            username+'","adid":"ED063999-948C-4B83-A80F-D412E3DB21DA","login_attempt_count":"0","phone_id":"A6ECB176-7695-4893-9185-A478D3B10BFD"}&ig_sig_key_version=5'
        resp = requests.post(url, headers=headers, data=data)
        if 'sessionid' in resp.cookies:
            session = re.findall(r'sessionid=(.*?) for', str(resp.cookies))[0]
            return render(request, 'free/resp-session.html', {"resp": session})
        return render(request, 'free/resp-session.html', {"resp": resp.text})


def index(request):
    model = Trending.objects.all().order_by('id_place')
    content = {"model": model}
    return render(request, 'index.html', content)


def show_products(request):
    model = Product.objects.all().order_by('id_place')
    groups = GroupProduct.objects.all()
    content = {"products": model, "groups": groups}
    return render(request, 'products.html', content)


def reset_instagram(request):
    if request.method == "GET":
        return render(request, 'free/reset-instagram.html')
    elif request.method == "POST":
        email_or_username = request.POST['email_or_username']
        url = 'https://www.instagram.com/accounts/account_recovery_send_ajax/'
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": "missing"
        }
        data = f'email_or_username={email_or_username}&recaptcha_challenge_field=&flow=fxcal&app_id=&source_account_id='
        resp = requests.post(url, headers=headers, data=data).json()['message']
        return render(request, 'free/resp-reset-instagram.html', {"resp": resp})


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
        content = {"userx": model, "profile": model2, "num": model.count()}
        return render(request, 'show-users.html', content)
    elif request.method == "POST":
        word = request.POST["word"]
        model = User.objects.filter(
            username__contains=word).order_by('-date_joined')
        model2 = Profile.objects.all()
        content = {"userx": model, "profile": model2}
        return render(request, 'show-users.html', content)


def edit_user(request, pk):
    obj = get_object_or_404(Profile, pk=pk)
    old = []
    for item in obj.product.all():
        old.append(item)

    if request.method == 'POST':
        form = EditProfile(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            new = get_object_or_404(Profile, pk=pk)
            for product in new.product.all():
                if product not in old:
                    print(obj)
                    dt = datetime.datetime.now()
                    
                    formatted_dt = dt.strftime('%Y-%m-%d %H:%M')
                    
                    productpaid = ProductsPaid.objects.create(user=obj.email_or_username,item=str(product),date=formatted_dt)
                    productpaid.save()
                    #print(product)
            return redirect('show-users')
    else:
        form = ProfileFormPK(instance=obj)
    return render(request, 'edit-user.html', {'form': form})

def productPaid(request):
    
    if request.method == "GET":
        users = ProductsPaid.objects.all()
        all = []
        pks = []
        for user in users:
            all.append(user.user + " : " + user.item +  " : " + str(user.date))
            pks.append(user.pk)
        all = all[::-1]
        pks = pks[::-1]
        content = { "all": all,"pks": pks}

        mylist = zip(all, pks)
        context = {'mylist': mylist}
        # context = {}
        # for item, id in zip(all, pks):
        #     context[item] = id
        
        return render(request, 'productpaid.html', context)
    elif request.method == "POST":
        word = request.POST["word"]
        model = ProductsPaid.objects.filter(user__contains=word)
        all = []
        for user in model:
            all.append(user.user)
            pks.append(user.pk)
        all = all[::-1]
        pks = pks[::-1]
        content = { "all": all,"pks": pks}
        return render(request, 'productpaid.html', content)
def delete_product_paid(request, pk):
    if request.method == "GET":
        return render(request, 'delete-product-paid.html')
    elif request.method == "POST":
        ProductsPaid.objects.filter(pk=pk).delete()
        return redirect('/productpaid/')
class EditUser(generic.UpdateView):
    model = Profile
    form = EditProfile()
    # fields = ['serial']
    fields = '__all__'
    template_name = "edit-user.html"
    success_url = '/show-users/'


class CreateProfile(generic.CreateView):
    model = Profile
    # ss = Profile.objects.all().order_by('-pk')

    form = EditProfile()
    # fields = ['serial']

    fields = '__all__'
    template_name = "edit-user.html"
    success_url = '/show-users/'


def info_instagram(user, session):
    headers = {
        "Host": "i.instagram.com",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 10.23.0 (iPhone11,2; iOS 12_1_4; ar_SA@calendar=gregorian; ar-SA; scale=3.00; gamut=wide; 1125x2001) AppleWebKit/420+",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"sessionid={session}"
    }
    resp = requests.get(
        f"https://i.instagram.com/api/v1/users/{user}/usernameinfo/", headers=headers).json()
    return resp


def download_story(id):
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
    }
    resp = requests.get(
        f"https://igs.sf-converter.com/api/stories/{id}", headers=Headers).text
    return json.loads(resp)


def download_video(link):
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "Content-Length": "50",
        "Alt-Used": "reelit.io",
    }
    data = '{"url":"'+link+'"}'
    req = requests.post("https://reelit.io/api/fetch",
                        data=data, headers=Headers)
    response = req.text
    resp = json.loads(response)
    return resp


def who_paid(request, name):
    if request.method == "GET":
        model = Product.objects.get(name=name)
        users = Profile.objects.all()
        all = []
        for user in users:
            if str(name) in str(user.product.all()):
                all.append(user.email_or_username)
        all = all[::-1]
        content = {"model": model, "users": users, "all": all}
        return render(request, 'who-paid.html', content)
    elif request.method == "POST":
        word = request.POST["word"]
        model = Profile.objects.filter(email_or_username__contains=word)
        all = []
        for user in model:
            if str(name) in str(user.product.all()):
                all.append(user.email_or_username)
        all = all[::-1]
        model2 = Profile.objects.all()
        content = {"all": all, "profile": model2}
        return render(request, 'who-paid.html', content)

def who_active(request):
    if request.method == "GET":
        users = WhoEditSerial.objects.all()
        all = []
        for user in users:
            all.append(user.user + " : " + str(user.date))
        all = all[::-1]
        content = { "all": all}
        return render(request, 'who-active.html', content)
    elif request.method == "POST":
        word = request.POST["word"]
        model = WhoEditSerial.objects.filter(user__contains=word)
        all = []
        for user in model:
            all.append(user.user)
        all = all[::-1]
        content = {"all": all}
        return render(request, 'who-paid.html', content)

def cart_view(request,item):
    model = Basket.objects.all()
    products = Product.objects.all()
    if request.user.username not in str(model):
        cart = Basket.objects.create(user=request.user.username)

    it = Basket.objects.get(user=request.user.username)
    allItems = []
    if item not in it.items:
        for iii in products:
            allItems.append(iii)
        if item in str(allItems):
            it.items = it.items + item + "|"
            Basket.objects.update(items=it.items)
    names = it.items.split('|')
    names.pop()

    all = 0
    for product in products:
        if product.name in names:
            all = all + product.price

    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    product = {
        'name': ",".join(names),
        'local_price':{
            'amount': str(all),
            'currency': 'USD'
            } ,
        'pricing_type': 'fixed_price',
    }

    if all > 0:
        #charge = client.charge.create(**product)
        charge = ""
    else:
        charge = ""
    content = {"new": it.items.split('|'),"products":products,"all":all,"charge":charge}
    return render(request,'basket.html',content)
def delete_cart(request):
    if request.method == "GET":
        return render(request, 'delete-card.html')
    elif request.method == "POST":
        Basket.objects.filter(user=request.user.username).delete()
        return redirect('/tools/')
    
from django.contrib.admin.views.decorators import user_passes_test

def admin_required(view_func):
    """
    Decorator for views that checks that the user is an admin.
    """
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/admin/login/',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func
# def basket_view(request,item):
#     model = Basket.objects.all()
#     form = CardForm
#     print(model)
#     if request.user.username in str(model):
#         products = Product.objects.all()
#         for product in products:
#             if product.name == item:
#                 #card.items.set([product.id])
#                 new = Basket.objects.get(id=product.id)
#                 new.items.set([product.id])
#                 new.save()
#     else:
#         card = Basket.objects.create(user=request.user.username)
#         products = Product.objects.all()
#         for product in products:
#             if product.name == item:
#                 card.items.set([product.id])
#         card.save()
#     model = Basket.objects.all()
#     content = {"model": model,"form":form}
#     return render(request,'basket.html',content)
# def initiate_payment(request):
#     paypalrestsdk.configure({
#         "mode": "live", # Change to "live" for production
#         "client_id": "AZpt5wQM3iptzOsEiBwerlcwL64Cw6AkgrLFKHtGJMDDa-m1IxSZeAJZT6WZ4Rx3G7bKMamqLb9GbTY2",
#         "client_secret": "EGG5ZxmqLZHOFVPdsmAL0gQ7TK2fT0mPNX_28uB5mZTzsJ69GWb9Y89mKehE8126PIUaT0U_NrrNJsKj"
#     })

#     payment = paypalrestsdk.Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": "http://127.0.0.1:8000/execute_payment/",
#             "cancel_url": "http://127.0.0.1:8000/cancel_payment/"
#         },
#         "transactions": [{
#             "amount": {
#                 "total": "2.00",
#                 "currency": "USD"
#             },
#             "description": "Example payment"
#         }]
#     })

#     if payment.create():
#         for link in payment.links:
#             if link.method == "REDIRECT":
#                 redirect_url = str(link.href)
#                 return redirect(redirect_url)
#     else:
#         print(payment.error)
#         return HttpResponse("Error while creating payment.")
# def execute_payment(request):
#     paypalrestsdk.configure({
#         "mode": "sandbox", # Change to "live" for production
#         "client_id": "AZpt5wQM3iptzOsEiBwerlcwL64Cw6AkgrLFKHtGJMDDa-m1IxSZeAJZT6WZ4Rx3G7bKMamqLb9GbTY2",
#         "client_secret": "EGG5ZxmqLZHOFVPdsmAL0gQ7TK2fT0mPNX_28uB5mZTzsJ69GWb9Y89mKehE8126PIUaT0U_NrrNJsKj"
#     })

#     payment_id = request.GET.get("paymentId")
#     payer_id = request.GET.get("PayerID")

#     payment = paypalrestsdk.Payment.find(payment_id)

#     if payment.execute({"payer_id": payer_id}):
#         return HttpResponse("Payment successful.")
#     else:
#         print(payment.error)
#         return HttpResponse("Error while executing payment.")

# def cancel_payment(request):
#     return HttpResponse("Payment cancelled.")
