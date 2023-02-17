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
    content = {"products":model}
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
    return render(request,'info-product.html',{"id": model,"charge": charge})

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


# def success_view(request):
    
#     return render(request, 'success.html')

# def cancel_view(request):
#     return render(request, 'cancel.html')


# @csrf_exempt
# @require_http_methods(['POST'])
# def coinbase_webhook(request):
#     logger = logging.getLogger(__name__)

#     request_data = request.body.decode('utf-8')
#     request_sig = request.headers.get('X-CC-Webhook-Signature', None)
#     webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

#     try:
#         event = Webhook.construct_event(request_data, request_sig, webhook_secret)

#         # List of all Coinbase webhook events:
#         # https://commerce.coinbase.com/docs/api/#webhooks

#         if event['type'] == 'charge:confirmed':
#             logger.info('Payment confirmed.')
#             customer_id = event['data']['metadata']['customer_id'] # new
#             customer_username = event['data']['metadata']['customer_username'] # new

#     except (SignatureVerificationError, WebhookInvalidPayload) as e:
#         return HttpResponse(e, status=400)

#     logger.info(f'Received event: id={event.id}, type={event.type}')
#     return HttpResponse('ok', status=200)