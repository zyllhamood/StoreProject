from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin
from .views import admin_required

# Register your models here.


class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('dis',)

class ProfileInline(admin.StackedInline):
    model = Profile
    #fields = ['username','email','product']
    can_delete = False
    verbose_name_plural = 'Profile'
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product, SomeModelAdmin)
admin.site.register(GroupProduct)
admin.site.register(RDP)
admin.site.register(Trending)
admin.site.register(Profile)
admin.site.register(WhoEditSerial)
admin.site.register(Basket)
admin.site.register(Serial)
admin.site.login = admin_required(admin.site.login)
