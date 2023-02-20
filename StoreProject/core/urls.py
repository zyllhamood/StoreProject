from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('api/products/',ProductView.as_view()),
    path('api/products/<int:pk>',ProductViewPK.as_view()),
    path('',home,name='home'),
    path('info/<int:pk>',info,name='info'),
    path('new/',login_required(NewProduct.as_view())),
    path('edit/<int:pk>',login_required(EditProduct.as_view()),name = 'edit'),
    path('groups/<str:title>',groups_view,name='group-url'),
    #path('payment/<int:pk>',payment_view)
]
