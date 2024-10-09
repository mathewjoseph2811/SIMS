from django.urls import path
from .views import *

urlpatterns = [
    path('', ItemMasterAPI.as_view(), name='create_item'),
    path('<int:item_id>/', GetItem.as_view(), name='get_item'),
]