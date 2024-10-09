from django.contrib import admin

# Register your models here.
from .models import ItemMaster

@admin.register(ItemMaster)
class ItemMasterAdmin(admin.ModelAdmin):
    list_display = ('vchr_item_code','vchr_item_name','txt_description','dbl_price','int_quantity','dat_created','dat_updated','bln_active')
    search_fields = ('vchr_item_code','vchr_item_name')
    list_filter = ('bln_active',)


    