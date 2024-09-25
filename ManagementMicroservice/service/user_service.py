from ManagementMicroservice.custom_helpers.status_code import *
from ManagementMicroservice.custom_helpers.model_serializers_helpers import CustomExceptionHandler, salt_and_hash, generate_token_pair, validate_token
from ManagementMicroservice.models import *
from ManagementMicroservice.custom_helpers.model_serializers_helpers import create_update_model_serializer
import uuid

def password_verification(user_object, secret):

    user_uuid = user_object.first().uuid_user
    password = user_object.first().password_hash
    user_id = user_object.first().id

    refresh_token_obj = RefreshToken.objects.filter(user_id=user_id).first()

    if password == salt_and_hash(user_uuid, secret).upper():
        access_token, refresh_token = generate_token_pair(user_object)

        if refresh_token_obj:
            refresh_token = refresh_token_obj.refresh_token
        else:
            RefreshToken.objects.create(refresh_token=refresh_token, user_id=user_id)
    else:
        raise CustomExceptionHandler(ErrorClass.invalid_valid_credentials)

    return access_token, refresh_token


def user_signup_service(request_data):
    
    from ManagementMicroservice.serializers.user_serializer import HeadSignUpSerializer

    password = request_data.get('password')

    if request_data.get('email_id'):
        obj = UserModel.objects.filter(email_id__iexact=request_data.get('email_id'))

        if len(obj) > 0:
            raise CustomExceptionHandler(ErrorClass.email_exists) 

    user_uuid = uuid.uuid4()

    secret_hash = salt_and_hash(str(user_uuid), password)
    request_data['password_hash'] = secret_hash.upper()
    request_data['uuid_user'] = str(user_uuid)

    final_data = {}

    signup_data_instance = create_update_model_serializer(HeadSignUpSerializer,request_data,partial=True)

    if signup_data_instance:
        serializer_obj = HeadSignUpSerializer(signup_data_instance).data
        final_data = final_data.update(serializer_obj)
    
    return get_response(success, data=final_data)


def user_login_service(request_data):

    from ManagementMicroservice.serializers.user_serializer import UserLoginRequestSerializer

    serialized_data = UserLoginRequestSerializer(data=request_data)

    if not serialized_data.is_valid():
        raise CustomExceptionHandler(generic_error_3)

    email_id = serialized_data.data.get('email_id')
    password =  serialized_data.data.get('password')

    user_obj = UserModel.objects.filter(email_id__iexact=email_id,status=STATUS_ACTIVE)

    if not user_obj:
        raise CustomExceptionHandler(ErrorClass.user_not_found)

    if len(user_obj) > 1:
        raise CustomExceptionHandler(ErrorClass.email_exists)

    access_token, refresh_token = password_verification(user_obj, password)

    return get_response(success, data={"access_token": access_token, "refresh_token": refresh_token})
