import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from ManagementMicroservice.custom_helpers.status_code import get_response, generic_error_2
from ManagementMicroservice.custom_helpers.model_serializers_helpers import CustomExceptionHandler
from ManagementMicroservice.serializers.user_serializer import UserLoginRequestSerializer, UserLoginResponseSerializer, \
                                                            UserSignUpRequestSerializer, UserSignUpResponseSerializer
from ManagementMicroservice.custom_helpers.custom_decorator import custom_api_view
from ManagementMicroservice.service.user_service import user_login_service, user_signup_service

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=UserSignUpRequestSerializer,
    responses={"200": UserSignUpResponseSerializer},
    operation_id="User Sign Up"
)
@api_view(["POST"])
def user_signup_view(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for user signup")
        response_obj = user_signup_service(request.data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in user signup url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in user signup url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in user signup --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body=UserLoginRequestSerializer,
    responses={"200": UserLoginResponseSerializer},
    operation_id="User Login"
)
@api_view(["POST"])
def user_login_view(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for user login")
        response_obj = user_login_service(request.data)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in user login: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in user login {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in user login --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)
