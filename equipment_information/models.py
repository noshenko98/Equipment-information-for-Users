from django.contrib.auth.models import AbstractUser
from django.db import models

from equipment_information_for_users import settings


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.country})"


class User(AbstractUser):
    favorite_equipment = models.ManyToManyField("Equipment",
                                                blank=True,
                                                related_name="favourite_equipment")

    def __str__(self):
        return f"{self.username}"


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    tech_specifications = models.JSONField(default=dict,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    manufacturer = models.ForeignKey(Manufacturer,
                                     on_delete=models.CASCADE,
                                     related_name="equipment")
    category = models.ForeignKey(EquipmentCategory,
                                 on_delete=models.CASCADE,
                                 related_name="equipment")
    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.model})"


class Commentary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="comments")
    equipment_post = models.ForeignKey(Equipment,
                             on_delete=models.CASCADE,
                             related_name="comments")
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"Comment by {self.user} on {self.equipment_post}"
