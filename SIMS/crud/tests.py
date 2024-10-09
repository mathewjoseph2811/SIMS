from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ItemMaster
from django.urls import reverse

class ItemMasterTests(TestCase):

    def setUp(self):
        # Create a user to associate with the item
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.client = APIClient() 
        
        # Obtain a JWT token for the test user
        self.token = RefreshToken.for_user(self.user).access_token
        
        # Set the authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_create_item_master(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM001',
            vchr_item_name='Test Item',
            txt_description='This is a test item.',
            dbl_price=10.99,
            int_quantity=100,
            fk_created=self.user
        )
        self.assertEqual(item.vchr_item_code, 'ITEM001')
        self.assertEqual(item.vchr_item_name, 'Test Item')
        self.assertEqual(item.txt_description, 'This is a test item.')
        self.assertEqual(item.dbl_price, 10.99)
        self.assertEqual(item.int_quantity, 100)
        self.assertEqual(item.fk_created, self.user)
        self.assertTrue(item.bln_active)

    def test_item_master_str(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM002',
            vchr_item_name='Another Item',
            txt_description='This is another test item.',
            dbl_price=20.99,
            int_quantity=50,
            fk_created=self.user
        )
        self.assertEqual(str(item), 'Another Item')

    def test_item_master_unique_code(self):

        ItemMaster.objects.create(
            vchr_item_code='ITEM003',
            vchr_item_name='Unique Item',
            txt_description='This is a unique item.',
            dbl_price=30.50,
            int_quantity=10,
            fk_created=self.user
        )
        with self.assertRaises(Exception):
            ItemMaster.objects.create(
                vchr_item_code='ITEM003',  # Duplicate code
                vchr_item_name='Another Unique Item',
                txt_description='This is another unique item.',
                dbl_price=35.00,
                int_quantity=5,
                fk_created=self.user
            )

    def test_item_master_default_active(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM004',
            vchr_item_name='Active Item',
            txt_description='This is an active item.',
            dbl_price=15.75,
            int_quantity=25,
            fk_created=self.user
        )
        self.assertTrue(item.bln_active)

    def test_edit_item_master(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM005',
            vchr_item_name='Edit Item',
            txt_description='This item will be edited.',
            dbl_price=12.00,
            int_quantity=75,
            fk_created=self.user
        )
        
        update_data = {
            'vchr_item_code': 'ITEM005',
            'vchr_item_name': 'Edited Item',
            'txt_description': 'This item has been edited.',
            'dbl_price': 20.00,
            'int_quantity': 75,
            'fk_created': self.user.id,
        }

        response = self.client.put(reverse('get_item', args=[item.id]), data=update_data, format='json')

        self.assertEqual(response.status_code, 200)

        updated_item = ItemMaster.objects.get(id=item.id)
        self.assertEqual(updated_item.vchr_item_name, 'Edited Item')
        self.assertEqual(updated_item.dbl_price, 20.00)

    def test_delete_item_master(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM006',
            vchr_item_name='Delete Item',
            txt_description='This item will be deleted.',
            dbl_price=5.50,
            int_quantity=30,
            fk_created=self.user
        )
        self.assertTrue(ItemMaster.objects.filter(id=item.id).exists())

        response = self.client.delete(reverse('get_item', args=[item.id]))
        self.assertEqual(response.status_code, 204)  # Check for successful deletion

        self.assertFalse(ItemMaster.objects.filter(id=item.id).exists())

    def test_view_item_master(self):

        item = ItemMaster.objects.create(
            vchr_item_code='ITEM007',
            vchr_item_name='View Item',
            txt_description='This item will be viewed.',
            dbl_price=25.00,
            int_quantity=50,
            fk_created=self.user
        )

        response = self.client.get(reverse('get_item', args=[item.id]))

        self.assertEqual(response.status_code, 200)

        fetched_item = ItemMaster.objects.get(id=item.id)
        self.assertEqual(fetched_item.vchr_item_code, item.vchr_item_code)
        self.assertEqual(fetched_item.vchr_item_name, item.vchr_item_name)
        self.assertEqual(fetched_item.txt_description, item.txt_description)
        self.assertEqual(fetched_item.dbl_price, item.dbl_price)
        self.assertEqual(fetched_item.int_quantity, item.int_quantity)
        self.assertEqual(fetched_item.fk_created, item.fk_created)

    def test_delete_non_existing_item_master(self):

        non_existing_id = 999  # Assuming this ID does not exist
        
        initial_count = ItemMaster.objects.count()

        response = self.client.delete(reverse('get_item', args=[non_existing_id]))
        
        self.assertEqual(response.status_code, 404)

        self.assertEqual(ItemMaster.objects.count(), initial_count)

    def test_update_non_existing_item_master(self):
        non_existing_id = 999  # Assuming this ID does not exist
        
        update_data = {
            'vchr_item_code': 'ITEM005',
            'vchr_item_name': 'Updated Item',
            'txt_description': 'This item does not exist.',
            'dbl_price': 25.99,
            'int_quantity': 10,
            'fk_created': self.user.id,
        }

        response = self.client.put(reverse('get_item', args=[non_existing_id]), data=update_data, format='json')

        self.assertEqual(response.status_code, 404)

    def test_view_non_existing_item_master(self):
        non_existing_id = 999  # Assuming this ID does not exist

        response = self.client.get(reverse('get_item', args=[non_existing_id]))

        self.assertEqual(response.status_code, 404)
