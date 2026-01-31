from django.shortcuts import render
from .models import Component, InventoryLevel

def component_list(request):
    return render(request, "atmio/inventory/component_list.html")

def component_table(request):
     # Get the "sort" query parameter from the URL
    sort_field = request.GET.get("sort", "id")  # default sort by id

    # Map allowed sort fields to actual model fields
    allowed_sort_fields = {
        "identifier": "identifier",
        "inventory_level": "inventory_level__name",
    }

    order_by = allowed_sort_fields.get(sort_field, "id")

    # Fetch components sorted
    components = Component.objects.select_related("inventory_level").order_by(order_by)

    return render(request, "atmio/inventory/component_table.html", {"components": components})

def component_create(request):
    inventory_levels = InventoryLevel.objects.all()
    if request.method == "POST":
        identifier = request.POST.get("identifier")
        description = request.POST.get("description")
        level_id = request.POST.get("inventory_level")
        level = InventoryLevel.objects.get(id=level_id)
        Component.objects.create(identifier=identifier, description=description, inventory_level=level)
        components = Component.objects.all()
        return render(request, "atmio/inventory/component_table.html", {"components": components})
    return render(request, "atmio/inventory/component_form.html", {"inventory_levels": inventory_levels})
