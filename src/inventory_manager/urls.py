from django.urls import path
from inventory_manager import views

urlpatterns = [
    path("", views.component_list, name="component_list"),
    path("table/", views.component_table, name="component_table"),
    path("create/", views.component_create, name="component_create"),
]
