from django.db import models
from ManagementMicroservice.custom_helpers.model_serializers_helpers import AddCommonField
from ManagementMicroservice.models.user_model import UserModel

class CommonInventoryModel(AddCommonField):

    id = models.BigAutoField(primary_key=True)
    uuid_user = models.TextField(null=False, unique=True)
    user = models.ForeignKey(UserModel, related_name='inventory_item', on_delete=models.RESTRICT, null=False)
    item_name = models.CharField(max_length=255, null=False)
    item_description = models.TextField(null=False)
    item_quantity = models.IntegerField(null=False)
    item_price = models.FloatField(null=False)

    class Meta:
        abstract = True


class InventoryModel(CommonInventoryModel):

    class Meta:
        db_table = "ums_inventory_model"