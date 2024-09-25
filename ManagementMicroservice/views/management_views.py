import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from ManagementMicroservice.custom_helpers.status_code import get_response, generic_error_2
from ManagementMicroservice.custom_helpers.model_serializers_helpers import CustomExceptionHandler
from ManagementMicroservice.serializers.inventory_serializer import RequestInventorySerializer, ResponseInventorySerializer, \
                                                                    GetInventoryItemResponseSerializer, InventoryDeleteSerializerResponse
from ManagementMicroservice.service.inventory_service import crud_inventory_item_service, get_inventory_item_service, delete_inventory_item_service

logger = logging.getLogger("django")


@csrf_exempt
@swagger_auto_schema(
    methods=['post'],
    request_body= RequestInventorySerializer,
    responses={"200": ResponseInventorySerializer},
    operation_id="Inventory Item CRUD"
)
@api_view(["POST"])
def inventory_create_item_view(request):
    response_obj = None

    try:
        logger.debug(f"{request.data}, request for create update inventory")
        response_obj = crud_inventory_item_service(request)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in create update inventory url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in create update inventory url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in create update inventory --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


@swagger_auto_schema(
    method='get',
    responses={
        200: GetInventoryItemResponseSerializer
    },
    operation_summary="Get Inventory Item",
    operation_description="Retrieve an inventory item by its ID."
)

@api_view(["GET"])
def get_inventory_item_view(request, id):
    response_obj = None

    try:
        logger.info(request, "request for get purchase order")        
        response_obj = get_inventory_item_service(request, id)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in get inventory url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in get inventory url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in get inventory --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)

@swagger_auto_schema(
    method='delete',
    responses={
        200: InventoryDeleteSerializerResponse
    },
    operation_summary="Delete Inventory Item",
)
@api_view(["DELETE"])
def delete_inventory_item_view(request, id):
    response_obj = None

    try:
        logger.info(request, "request for purchase order delete")
        response_obj = delete_inventory_item_service(request, id)

    except CustomExceptionHandler as e:
        logger.exception(f"Custom Exception in delete inventory url: {e}")
        response_obj = get_response(eval(str(e)))

    except Exception as e:
        logger.exception(f"Exception in delete inventory url {e}")
        response_obj = get_response(generic_error_2)

    logger.info("response in delete inventory --> %s", response_obj)
    return JsonResponse(response_obj, safe=False)


