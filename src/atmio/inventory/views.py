from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Component, InventoryLevel

from django.db import IntegrityError
from django.http import HttpResponse

PAGINATION_LIMIT = 10


def _get_or_post_query_param(request, key: str) -> str | None:
    return request.GET.get(key) or request.POST.get(key)

def component_list(request):
    inventory_levels = InventoryLevel.objects.all()
    return render(
        request,
        "atmio/inventory/component_list.html",
        {"inventory_levels": inventory_levels},
    )

def component_table(request):
    sort = _get_or_post_query_param(request, key="sort") or "id"
    direction = _get_or_post_query_param(request, key="dir") or "asc"
    filter_identifier = _get_or_post_query_param(request, key="filter_identifier") or ""
    filter_inventory_level = _get_or_post_query_param(request, key="filter_inventory_level") or ""
    page_number = _get_or_post_query_param(request, key="page") or 1

    sort_map = {"identifier": "identifier", "inventory_level": "inventory_level__name"}
    order_by = sort_map.get(sort, "id")
    if direction == "desc":
        order_by = f"-{order_by}"

    qs = Component.objects.select_related("inventory_level").all()

    # Filter by identifier
    if filter_identifier:
        qs = qs.filter(identifier__icontains=filter_identifier)

    # Optimized hierarchical inventory level filtering
    if filter_inventory_level:
        # Prefetch all levels in one query
        all_levels = InventoryLevel.objects.all()
        level_map = {}
        for lvl in all_levels:
            level_map.setdefault(lvl.parent_id, []).append(lvl.id)

        # Recursive function in memory
        def get_descendants(level_id):
            ids = [int(level_id)]
            for child_id in level_map.get(int(level_id), []):
                ids.extend(get_descendants(child_id))
            return ids

        # Get all relevant level IDs
        level_ids = get_descendants(filter_inventory_level)
        qs = qs.filter(inventory_level_id__in=level_ids)

    # Apply sorting
    qs = qs.order_by(order_by)

    # Pagination
    paginator = Paginator(qs, PAGINATION_LIMIT)
    page_obj = paginator.get_page(page_number)

    return render(request, "atmio/inventory/component_table.html", {
        "components": page_obj.object_list,
        "page_obj": page_obj,
        "current_sort": sort,
        "current_dir": direction,
        "current_filter_identifier": filter_identifier,
        "current_inventory_level": filter_inventory_level
    })



def component_create(request):
    inventory_levels = InventoryLevel.objects.all()

    if request.method == "POST":
        identifier = request.POST.get("identifier", "")
        description = request.POST.get("description", "")
        level_id = request.POST.get("inventory_level", "")

        try:
            Component.objects.create(
                identifier=identifier,
                description=description,
                inventory_level_id=level_id,
            )
        except IntegrityError:
            return render(
                request,
                "atmio/inventory/component_form.html",
                {
                    "inventory_levels": inventory_levels,
                    "error_message": "A component with this identifier already exists.",
                    "form_data": {
                        "identifier": identifier,
                        "description": description,
                        "inventory_level": level_id,
                    }
                }
            )

        # Success: empty response + trigger
        response = HttpResponse('<div style="display:none;"></div>')
        response["HX-Trigger"] = "inventoryUpdated"
        return response

    return render(
        request,
        "atmio/inventory/component_form.html",
        {"inventory_levels": inventory_levels, "form_data": {}}
    )
