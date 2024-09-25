from rest_framework import serializers
from ManagementMicroservice.models import *
from django.db.transaction import atomic
from ManagementMicroservice.custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict \
    , CustomExceptionHandler, comman_create_update_services, common_checking_and_passing_value_from_list_dict
from ManagementMicroservice.custom_helpers.consts import *
import re
from ManagementMicroservice.custom_helpers.status_code import *


class HeadInventorySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    item_name = serializers.CharField(max_length=255, required=True)
    item_description = serializers.CharField(required=True)
    item_quantity = serializers.IntegerField(required=True)
    item_price = serializers.FloatField(required=True)

    class Meta:
        model = InventoryModel
        exclude = ("creation_date", "creation_by", "updation_date", "updation_by","status","uuid_user", "user",)

    def validate(self, data):
        data = super().validate(data)
        return {key: value for key, value in data.items() if value is not None}

    @atomic
    def create(self, validated_data):
        return comman_create_update_services(self, validated_data)

    @atomic
    def update(self, instance, validated_data):
        return comman_create_update_services(self, validated_data, instance)


    def to_representation(self, data):
        data = super().to_representation(data)
        return data 


class RequestInventorySerializer(HeadInventorySerializer):

    class Meta:
        model = InventoryModel
        exclude = ("creation_date", "creation_by", "updation_date", "updation_by","status","uuid_user", "user",)


class ResponseInventorySerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadInventorySerializer(required=False)

    class Meta:
        model = InventoryModel
        fields = ("status", "message", "data",)


# Get API Serializer
class GetInventoryItemResponseSerializer(serializers.Serializer): 
    
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = HeadInventorySerializer(required=False)

    class Meta:
        model = InventoryModel
        fields = ("status", "message", "data",)

# Delete API Serializer
class InventoryDeleteSerializerResponse(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    
    class Meta:
        model = InventoryModel
        fields = ("status", "message",)

