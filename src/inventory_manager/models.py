from django.db import models


class InventoryLevel(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Component(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    inventory_level = models.ForeignKey(InventoryLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.identifier
