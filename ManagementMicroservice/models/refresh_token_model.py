from django.db import models
from ManagementMicroservice.models import UserModel
from ManagementMicroservice.custom_helpers.model_serializers_helpers import AddCommonField


class CommonRefreshToken(AddCommonField):
    refresh_token = models.TextField(primary_key=True)
    user = models.ForeignKey(UserModel, related_name='refresh_user', on_delete=models.RESTRICT, null=False)

    class Meta:
        abstract = True


class RefreshToken(CommonRefreshToken):

    class Meta:
        db_table = "ums_refresh_token"
