from django.db import migrations

import random


def seed_inventory(apps, schema_editor):
    # Get models via apps.get_model
    InventoryLevel = apps.get_model("inventory_manager", "InventoryLevel")
    Component = apps.get_model("inventory_manager", "Component")

    # Root
    root = InventoryLevel.objects.create(name="Main Facility")

    # Level 1: Storage Tanks
    tanks = []
    for i in range(1, 6):  # 5 tanks
        tank = InventoryLevel.objects.create(name=f"Storage Tank {i}", parent=root)
        tanks.append(tank)

    # Level 2: Each tank has sections
    sections = []
    for tank in tanks:
        for j in range(1, 3):
            section = InventoryLevel.objects.create(
                name=f"{tank.name} Section {j}", parent=tank
            )
            sections.append(section)

    # Level 1: Pipelines
    pipelines = []
    for i in range(1, 2):
        pipe = InventoryLevel.objects.create(name=f"Pipeline {i}", parent=root)
        pipelines.append(pipe)

    # Level 2: Each pipeline has segments
    segments = []
    for pipe in pipelines:
        for j in range(1, 3):
            segment = InventoryLevel.objects.create(
                name=f"{pipe.name} Segment {j}", parent=pipe
            )
            segments.append(segment)

    all_levels = tanks + sections + pipelines + segments

    # Create components distributed randomly across levels
    for i in range(1, 50):
        level = random.choice(all_levels)
        Component.objects.create(
            identifier=f"C{i:04d}",
            description=f"Component {i} in {level.name}",
            inventory_level=level,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("inventory_manager", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_inventory),
    ]
