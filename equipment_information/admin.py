from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from equipment_information.models import (Manufacturer,
                                          Equipment,
                                          User,
                                          EquipmentCategory,
                                          Commentary)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id","name", "country",)
    search_fields = ("name",)
    list_filter = ("country",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("category", "manufacturer", "name", "model",)
    search_fields = ("name", "model",)
    list_filter = ("manufacturer", "category")
    ordering = ("price",)
    list_per_page = 10


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username",)
    list_per_page = 10
    fieldsets = UserAdmin.fieldsets + (
        ("Favorite equipment", {"fields": ("favorite_equipment",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Favorite equipment", {"fields": ("favorite_equipment",)}),)


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "equipment_post", "content")
    list_filter = ("user",)
    search_fields = ("content","equipment_post__name",)
