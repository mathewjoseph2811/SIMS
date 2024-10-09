from django.db import models
from django.contrib.auth.models import User

class ItemMaster(models.Model):
    vchr_item_code = models.CharField(max_length=20, unique=True)
    vchr_item_name = models.CharField(max_length=100)
    txt_description = models.TextField(blank=True, null=True)
    dbl_price = models.DecimalField(max_digits=10, decimal_places=2)
    int_quantity = models.IntegerField(default=0)
    dat_created = models.DateTimeField(auto_now_add=True)
    fk_created = models.ForeignKey(User, on_delete=models.CASCADE)
    dat_updated = models.DateTimeField(null=True)
    bln_active = models.BooleanField(default=True)

    def __str__(self):
        return self.vchr_item_name

    class Meta:
        db_table = 'item_master'  
        verbose_name = 'Item Master'
        verbose_name_plural = 'Item Masters'
