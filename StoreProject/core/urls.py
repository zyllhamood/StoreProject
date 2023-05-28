from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('api/products/',ProductView.as_view()),
    path('api/products/<int:pk>',ProductViewPK.as_view()),
    path('api/serial/',ProfileSerilaizerView.as_view()),
    
    path('tools/',tools,name='tools'),
    path('info/<str:name>',info,name='info'),
    path('new/',login_required(NewProduct.as_view()),name='new'),
    path('edit/<int:pk>',login_required(EditProduct.as_view()),name = 'edit'),
    path('groups/<str:title>',groups_view,name='group-url'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',login_page,name='loginurl'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logouturl'),
    path('profile/',login_required(ProfileView.as_view()),name='profile'),
    #path('userinfo/',profile_view,name='profile-view'),

    #path('edit-profile/<int:pk>',login_required(EditProfileView.as_view()),name='edit-profile'),
    path('edit-profile/<int:pk>',login_required(edit_profile),name='edit-profile'),

    path('rdp/',login_required(rdp_control),name='rdp'),
    path('rdp/<str:action>',login_required(action_rdp),name='action-rdp'),
    
    #path('add-user/',ProfileCreateView.as_view(),name='add-user'),
    #path('edit-user/<int:pk>',ProfileEditView.as_view(),name='edit-user'),

    path('free-services/',homeFreeTools),
    path('call-request/',call_request),
    path('build-request/',made_request),
    path('get-session/',get_session),
    path('',index,name='home'),
    path('products/',show_products),
    path('reset-instagram/',reset_instagram),

    path('show-users/',show_users,name='show-users'),
    #path('profile/<int:pk>',EditUser.as_view(),name='edit-user'),
    path('profile/<int:pk>',edit_user,name='edit-user'),
    path('profile/new/',CreateProfile.as_view(),name='new-profile'),

    path('delete-product/<int:pk>',delete_product,name='delete-product'),

    path('who-paid/<str:name>',who_paid,name='who-paid'),
    path('who-active/',who_active,name='who-active'),

    path('cart/<str:item>',cart_view,name='cart'),
    path('delete-cart/',delete_cart,name='delete-cart'),

    path('productpaid/',productPaid,name='productpaid'),
    path('delete-product-paid/<int:pk>',delete_product_paid,name='delete-product-paid')


    #path('bot/',bot_instagram)

    # path("paypal/", initiate_payment, name="initiate_payment"),
    # path("execute_payment/", execute_payment, name="execute_payment"),
    # path("cancel_payment/", cancel_payment, name="cancel_payment"),

   
    
    
    #path('payment/<int:pk>',payment_view)
]
