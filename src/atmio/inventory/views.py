from django.shortcuts import render
from .models import Component, InventoryLevel


def component_list(request):
    inventory_levels = InventoryLevel.objects.all()
    return render(
        request,
        "atmio/inventory/component_list.html",
        {"inventory_levels": inventory_levels},
    )


def component_table(request):
    sort = request.GET.get("sort", "id")
    direction = request.GET.get("dir", "asc")
    filter_identifier = request.GET.get("filter_identifier", "")
    filter_inventory_level = request.GET.get("filter_inventory_level", "")

    sort_map = {"identifier": "identifier",
                "inventory_level": "inventory_level__name"}
    order_by = sort_map.get(sort, "id")
    if direction == "desc":
        order_by = f"-{order_by}"

    components = Component.objects.select_related("inventory_level").all()

    if filter_identifier:
        components = components.filter(identifier__icontains=filter_identifier)
    if filter_inventory_level:
        components = components.filter(inventory_level_id=filter_inventory_level)

    components = components.order_by(order_by)

    return render(request, "atmio/inventory/component_table.html", {
        "components": components,
        "current_sort": sort,
        "current_dir": direction,
        "current_filter_identifier": filter_identifier,
        "current_inventory_level": filter_inventory_level
    })

def component_create(request):
    inventory_levels = InventoryLevel.objects.all()

    if request.method == "POST":
        identifier = request.POST.get("identifier")
        description = request.POST.get("description")
        level_id = request.POST.get("inventory_level")

        Component.objects.create(
            identifier=identifier,
            description=description,
            inventory_level_id=level_id,
        )

        # Return ONLY table rows (HTMX swap target)
        return component_table(request)

    return render(
        request,
        "atmio/inventory/component_form.html",
        {"inventory_levels": inventory_levels},
    )
