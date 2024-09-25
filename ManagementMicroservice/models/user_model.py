from django.db import models
from ManagementMicroservice.custom_helpers.model_serializers_helpers import AddCommonField

class CommonUserModel(AddCommonField):

    id = models.BigAutoField(primary_key=True)
    uuid_user = models.TextField(null=False, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email_id = models.TextField(null=False, unique=True)
    mobile_no = models.CharField(null=False, unique=True)
    password_hash = models.TextField(null=False)

    class Meta:
        abstract = True


class UserModel(CommonUserModel):

    class Meta:
        db_table = "ums_user_model"