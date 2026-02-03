from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import ListView
from django.http import HttpResponse

from inventory_manager.models import Component, InventoryLevel
from inventory_manager.services.inventory import get_descendant_inventory_level_ids
from inventory_manager.forms import ComponentForm


PAGINATION_LIMIT = 10


def component_list(request):
    inventory_levels = InventoryLevel.objects.all()
    return render(
        request,
        "inventory_manager/component_list.html",
        {"inventory_levels": inventory_levels},
    )


class ComponentTableView(ListView):
    model = Component
    template_name = "inventory_manager/component_table.html"
    context_object_name = "components"
    paginate_by = PAGINATION_LIMIT

    SORT_MAP = {
        "identifier": "identifier",
        "inventory_level": "inventory_level__name",
    }

    def get_queryset(self):
        request = self.request

        sort = request.GET.get("sort", "id")
        direction = request.GET.get("dir", "asc")
        filter_identifier = request.GET.get("filter_identifier", "")
        filter_inventory_level = request.GET.get("filter_inventory_level")

        order_by = self.SORT_MAP.get(sort, "id")
        if direction == "desc":
            order_by = f"-{order_by}"

        qs = Component.objects.select_related("inventory_level").order_by(order_by)

        if filter_identifier:
            qs = qs.filter(identifier__icontains=filter_identifier)

        if filter_inventory_level:
            qs = qs.filter(
                inventory_level_id__in=get_descendant_inventory_level_ids(
                    int(filter_inventory_level)
                )
            )

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        request = self.request

        ctx.update(
            {
                "current_sort": request.GET.get("sort", "id"),
                "current_dir": request.GET.get("dir", "asc"),
                "current_filter_identifier": request.GET.get("filter_identifier", ""),
                "current_inventory_level": request.GET.get(
                    "filter_inventory_level", ""
                ),
            }
        )
        return ctx


class ComponentCreateView(CreateView):
    model = Component
    form_class = ComponentForm
    template_name = "inventory_manager/component_form.html"

    def form_valid(self, form):
        self.object = form.save()
        response = HttpResponse('<div style="display:none;"></div>')
        response["HX-Trigger"] = "inventoryUpdated"
        return response
