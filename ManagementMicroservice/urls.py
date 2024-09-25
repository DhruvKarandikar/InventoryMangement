from django.urls import path
from .views import *

urlpatterns = [
    # User Path API
    path('user/user_login', user_login_view, name='user_sign_in'),
    path('user/user_signup', user_signup_view, name='user_sign_up'),

    # Inventory path API
    path('inventory/items', inventory_create_item_view, name='create_item'),
    path('inventory/get_items/<int:id>', get_inventory_item_view, name='get_item'),
    path('inventory/delete_items/<int:id>', delete_inventory_item_view, name='delete_item'),
]
