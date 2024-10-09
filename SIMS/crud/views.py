from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from SIMS import ins_logger
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ItemMaster
from datetime import datetime
import sys
from .serializers import ItemMasterSerializer
from django.core.cache import cache

class ItemMasterAPI(APIView):
    # permission_classes = [AllowAny]
    def post(self,request):
        try:
            dct_data = request.data

            if not dct_data.get('vchr_item_code'):
                return Response( 'Item code is mandatory', status = 400)

            if not dct_data.get('vchr_item_name'):
                return Response( 'Item name is mandatory', status = 400)

            if ItemMaster.objects.filter(vchr_item_code = dct_data.get('vchr_item_code'),bln_active = True).exists():
                return Response( 'Item code already exists', status = 400)

            if ItemMaster.objects.filter(vchr_item_name = dct_data.get('vchr_item_name'),bln_active = True).exists():
                return Response( 'Item name already exists', status = 400)

            ins_item = ItemMaster(
                vchr_item_code = dct_data.get('vchr_item_code'),
                vchr_item_name = dct_data.get('vchr_item_name'),
                txt_description = dct_data.get('txt_description'),
                dbl_price = dct_data.get('dbl_price'),
                int_quantity = dct_data.get('int_quantity'),
                dat_created = datetime.now(),
                bln_active = True,
                fk_created_id = request.user.id if request.user.id else 1
            )

            # Test data kit = {"vchr_item_code": "ITEM001","vchr_item_name": "Sample Item","txt_description": "This is a sample item for testing purposes.","dbl_price": 99.99,"int_quantity": 50}


            ins_item.save()
            serializer = ItemMasterSerializer(ins_item)

            return Response( {"message": "Item added successfully.",'data': serializer.data}, status = 200)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({"error": str(e)}, status = 500)



class GetItem(APIView):
    # permission_classes = [AllowAny]
    def get(self, request, item_id):
        try:
            # Checking if the item is already cached in Redis
            str_cache_key = f"item_{item_id}"  
            ins_cached_item = cache.get(str_cache_key)
            
            if ins_cached_item:
                return Response(ins_cached_item, status = 200)

            else:
                ins_item = ItemMaster.objects.filter(id = item_id).values('id','vchr_item_code','vchr_item_name','txt_description','dbl_price','int_quantity','dat_created','fk_created_id','dat_updated','bln_active','fk_created_id__username')

                if ins_item:
                    # Store the item in Redis with a timeout of  1 hour
                    cache.set(str_cache_key, ins_item, timeout = 3600)

                    return Response(ins_item, status = 200)

                else:
                    return Response({"error": "Item not found."}, status = 404)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({"error": str(e)}, status = 500)


    def delete(self, request, item_id):
        try:
            item = ItemMaster.objects.get(id = item_id)

            if item:
                item.delete()
                str_cache_key = f"item_{item_id}"
                cache.delete(str_cache_key)
                return Response({"message": "Item deleted successfully."}, status = 204)

        except ItemMaster.DoesNotExist:
            return Response({"error": "Item not found."}, status = 404)
    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({"error": str(e)}, status = 500)


    def put(self, request, item_id):
        try:
            dct_data = request.data
            if not dct_data.get('vchr_item_code'):
                return Response( 'Item code is mandatory', status = 400)

            if not dct_data.get('vchr_item_name'):
                return Response( 'Item name is mandatory', status = 400)

            if ItemMaster.objects.filter(vchr_item_code = dct_data.get('vchr_item_code'),bln_active = True).exclude(id = item_id).exists():
                return Response( 'Item code already exists', status = 400)

            if ItemMaster.objects.filter(vchr_item_name = dct_data.get('vchr_item_name'),bln_active = True).exclude(id = item_id).exists():
                return Response( 'Item name already exists', status = 400)

            if not ItemMaster.objects.filter(id = item_id).exists():
                return Response( 'Item does not exists', status = 404)

            ins_item = ItemMaster.objects.filter(id = item_id).update(
                vchr_item_code = dct_data.get('vchr_item_code'),
                vchr_item_name = dct_data.get('vchr_item_name'),
                txt_description = dct_data.get('txt_description'),
                dbl_price = dct_data.get('dbl_price'),
                int_quantity = dct_data.get('int_quantity'),
                dat_updated = datetime.now(),
                bln_active = True,
                fk_created_id = request.user.id if request.user.id else 1
            )

            ins_updated_item = ItemMaster.objects.filter(id = item_id).values('id','vchr_item_code','vchr_item_name','txt_description','dbl_price','int_quantity','dat_created','fk_created_id','dat_updated','bln_active','fk_created_id__username')

            str_cache_key = f"item_{item_id}"
            cache.delete(str_cache_key)
            cache.set(str_cache_key, ins_updated_item, timeout=3600)


            return Response( {"message": "Item edited successfully.",'updated data': ins_updated_item}, status = 200)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({"error": str(e)}, status = 500)


    

        
        