from rest_framework import serializers
from .models import ItemMaster

class ItemMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMaster
        fields = '__all__'  # Or specify the fields you want to include