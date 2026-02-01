from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True  # Marks it as the first migration
    dependencies = []  # No dependencies, runs first

    operations = [
        migrations.CreateModel(
            name="InventoryLevel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("parent", models.ForeignKey(
                    "self", null=True, blank=True, on_delete=models.CASCADE
                )),
            ],
        ),
        migrations.CreateModel(
            name="Component",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("identifier", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("inventory_level", models.ForeignKey(
                    "InventoryLevel", on_delete=models.CASCADE
                )),
            ],
        ),
    ]
