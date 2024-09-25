from ManagementMicroservice.custom_helpers.status_code import *
from ManagementMicroservice.custom_helpers.model_serializers_helpers import CustomExceptionHandler, validate_token
from ManagementMicroservice.models import *
from ManagementMicroservice.custom_helpers.model_serializers_helpers import create_update_model_serializer


def crud_inventory_item_service(request):

    from ManagementMicroservice.serializers.inventory_serializer import HeadInventorySerializer

    token_data = validate_token(request)
    uuid_user = token_data.user_uuid
    user_id = token_data.user_id

    request_data = request.data
    
    final_data = {}

    inventory_obj = create_update_model_serializer(HeadInventorySerializer, request_data, partial=True, additional_data={"uuid_user": uuid_user, "user_id": user_id})

    if inventory_obj:

        serialized_obj = HeadInventorySerializer(inventory_obj).data
        final_data.update(serialized_obj)

    return get_response(success, data=final_data)
    
    
def get_inventory_item_service(request, item_id):

    from ManagementMicroservice.serializers.inventory_serializer import HeadInventorySerializer

    token_data = validate_token(request)
    uuid_user = token_data.user_uuid
    user_id = token_data.user_id

    inventory_obj = InventoryModel.objects.filter(id=item_id, uuid_user__iexact=uuid_user, status=STATUS_ACTIVE).first()

    obj = {}

    if inventory_obj:
        obj = HeadInventorySerializer(inventory_obj).data

    return get_response(success, data=obj)


def delete_inventory_item_service(request, item_id):
    token_data = validate_token(request)
    uuid_user = token_data.user_uuid
    user_id = token_data.user_id

    inventory_obj = InventoryModel.objects.filter(id=item_id, uuid_user__iexact=uuid_user, status=STATUS_ACTIVE).first()

    if not inventory_obj:
        raise CustomExceptionHandler(ErrorClass.item_obj_no_exist)

    inventory_obj.status = STATUS_INACTIVE
    inventory_obj.save()
    return get_response(success)

