from django.urls import path
from inventory_manager.views import (
    ComponentTableView,
    ComponentCreateView,
    component_list,
)

urlpatterns = [
    path("", component_list, name="component_list"),
    path("table/", ComponentTableView.as_view(), name="component_table"),
    path("create/", ComponentCreateView.as_view(), name="component_create"),
]
