from typing import Iterable
from inventory_manager.models import InventoryLevel


def get_descendant_inventory_level_ids(level_id: int) -> list[int]:
    levels = InventoryLevel.objects.all().values("id", "parent_id")

    children_map: dict[int | None, list[int]] = {}
    for lvl in levels:
        children_map.setdefault(lvl["parent_id"], []).append(lvl["id"])

    def walk(pk: int) -> Iterable[int]:
        yield pk
        for child in children_map.get(pk, []):
            yield from walk(child)

    return list(walk(level_id))
