from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('dis',)

admin.site.register(Product, SomeModelAdmin)
admin.site.register(GroupProduct)

