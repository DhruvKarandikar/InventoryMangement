from rest_framework import serializers
from ManagementMicroservice.models import *
from django.db.transaction import atomic
from ManagementMicroservice.custom_helpers.model_serializers_helpers import dict_get_key_from_value, help_text_for_dict \
    , CustomExceptionHandler, comman_create_update_services, common_checking_and_passing_value_from_list_dict
from ManagementMicroservice.custom_helpers.consts import *
import re
from ManagementMicroservice.custom_helpers.status_code import *

def password_regex(password):

    if len(password) < 8:
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'

    return re.match(pattern, password) is not None



#  User Login Serializer
class UserLoginRequestSerializer(serializers.Serializer):
    email_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = UserModel
        fields = ("email_id", "password",)
    
    def validate_email_id(self,value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
        if not re.fullmatch(regex, value):
            raise CustomExceptionHandler(ErrorClass.email_id_incorrect)  
        return value
    
    

class SigninDataResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
    
    class Meta:
        model = RefreshToken
        fields = ("access_token", "refresh_token",)


class UserLoginResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = SigninDataResponseSerializer(required=False) 

    class Meta:
        model = UserModel
        fields = ("status", "message","data",)



# User Signup serializer
class HeadSignUpSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    email_id = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)
    password_hash = serializers.CharField(required=True)

    class Meta:
        model = UserModel
        exclude = ("creation_date", "creation_by", "updation_date", "updation_by","status",)
        depth = 2


    def validate_uuid_user(self, value):
        if value in [None, "", 0]:
            raise CustomExceptionHandler(ErrorClass.uuid_user_none)

        if UserModel.objects.filter(uuid_user__iexact=value).exists():
            raise CustomExceptionHandler(ErrorClass.uuid_user_exists)

        return value

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


class UserSignUpRequestSerializer(HeadSignUpSerializer):
    password_hash = None
    password = serializers.CharField(required=True)
    
    class Meta:
        model = UserModel
        exclude = ("creation_date", "creation_by", "updation_date", "updation_by", "password_hash","status", "uuid_user",)

    def validate_email_id(self,value):
        
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  
        if not re.fullmatch(regex, value):
            raise CustomExceptionHandler(ErrorClass.email_id_incorrect)

        return value        

    def validate_password(self,value):

        if value:

            bool_regex = password_regex(value)

            if bool_regex == False:
                raise CustomExceptionHandler(ErrorClass.password_regex_error)

        return value
    

class UserSignUpResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField(help_text = "Status Code", required = False)
    message = serializers.CharField(help_text = "Status Message", required = False)
    data = UserSignUpRequestSerializer(required=False)

    class Meta:
        model = UserModel
        fields = ("status", "message", "data",)
