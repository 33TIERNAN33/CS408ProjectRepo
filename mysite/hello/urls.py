from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("inventory/", views.available_inventory, name="available_inventory"),
    path("requested/", views.requested_items, name="requested_items"),
    path("distributed/", views.distributed_items, name="distributed_items"),
]
