import copy
import logging
from django.test import Client, TestCase
from django.urls import reverse
from ManagementMicroservice.models import *
from ManagementMicroservice.custom_helpers.status_code import *
import json
from unittest import mock

logger = logging.getLogger("django")

class EmptyClass():
    None

def recreate_objects():
    user_obj = UserModel.objects.create(
        first_name = "dhruv",
        last_name = "karandikar",
        email_id = "dhruvkarandikar@gmail.com",
        mobile_no = "9130249999",
        password_hash = "30FD34B280A58078A0D50DF6A79B1D3B3315FEB166AB17BA8E511DF0C2DB8247",
        uuid_user="eab3dd75-ddd8-42df-a99b-a9d0df15b420"
    )
    refresh_token = RefreshToken.objects.create(
        refresh_token = "abcs",
        user_id = user_obj.id
    )
    item = InventoryModel.objects.create(
        uuid_user = user_obj.uuid_user,
        user_id = user_obj.id,
        item_name = "product 1",
        item_description = "good qaulty",
        item_quantity = 55,
        item_price = 1500.22
    )
    return user_obj, refresh_token, item

class TestCreateUpdateInventoryItem(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('create_item')

    def postReq(self, payload):
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")
    
    def common_test_call(self, data):
        response = self.postReq(data)
        content = json.loads(response.content)
        return content

    obj = EmptyClass()
    obj.user_uuid = "1"
    obj.user_id = 1
    @mock.patch("ManagementMicroservice.service.inventory_service.validate_token", return_value=obj)
    def test_inventory_create_update(self, *args, **kwargs):
        user_obj, refresh_token, item = recreate_objects()
        data = {
            "item_name": "product1",
            "item_description": "bad product",
            "item_quantity": 1,
            "item_price": 1000.44
        }
        data_copy = copy.deepcopy(data)
        actual_response = self.common_test_call(data_copy)
        expected_response = success[STATUS_CODE]
        logger.debug("actual_response %s", actual_response)
        self.assertEqual(actual_response['status'], expected_response)

