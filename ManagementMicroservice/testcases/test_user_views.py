import copy
import logging
from django.test import Client, TestCase
from django.urls import reverse
from ManagementMicroservice.models import *
from ManagementMicroservice.custom_helpers.status_code import *
import json

logger = logging.getLogger("django")


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
    return user_obj, refresh_token


class TestUserLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user_sign_in')

    def postReq(self, payload):
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")
    
    def common_test_call(self, data):
        response = self.postReq(data)
        content = json.loads(response.content)
        return content
    
    def test_user_login(self):
        user_obj, refresh_token = recreate_objects()
        data = {
            "email_id": "dhruvkarandikar@gmail.com",
            "password": "ABCabc123"
        }

        data_copy = copy.deepcopy(data)
        actual_response = self.common_test_call(data_copy)
        expected_response = success[STATUS_CODE]
        logger.debug("actual_response %s", actual_response)
        self.assertEqual(actual_response['status'], expected_response)




class TestUserSignup(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user_sign_up')

    def postReq(self, payload):
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")

    def common_test_call(self, data):
        response = self.postReq(data)
        content = json.loads(response.content)
        return content

    def test_user_signup(self):
        user_obj, refresh_token = recreate_objects()
        data = {
            "first_name": "Dhruv",
            "last_name": "Karandikar",
            "email_id": "dhruvkarandikar22@gmail.com",
            "mobile_no": "9130249440",
            "password": "ABCabc123"
        }

        data_copy = copy.deepcopy(data)
        actual_response = self.common_test_call(data_copy)
        expected_response = success[STATUS_CODE]
        logger.debug("actual_response %s", actual_response)
        self.assertEqual(actual_response['status'], expected_response)

