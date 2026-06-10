from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase, Client
from django.urls import reverse

from equipment_information.models import Manufacturer, EquipmentCategory, Equipment


class TestFormsSearch(TestCase):
    fixtures = ['equipment_data.json']
    PAGINATION = 5

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD1234>",
        )
        self.client.force_login(self.user)

    def test_forms_search_manufacturer(self, pag=PAGINATION):
        form_date = {
            "name": "as",
        }
        manufacturer = Manufacturer.objects.filter(
            name__icontains=form_date["name"])
        response = self.client.get(
            reverse("equipment_information:manufacturer-list"),
            form_date)
        self.assertEqual(list(response.context_data["manufacturer_list"]),
                         list(manufacturer)[:pag])

    def test_forms_search_equipment_category(self, pag=PAGINATION):
        form_date = {
            "name": "Lap",
        }
        equipment_category = EquipmentCategory.objects.filter(
            name__icontains=form_date["name"])
        response = self.client.get(
            reverse("equipment_information:equipments-category-list"),
            form_date)
        self.assertEqual(list(response.context_data["equipment_category_list"]),
                         list(equipment_category)[:pag])

    def test_forms_search_user(self, pag=PAGINATION):
        form_date = {
            "username": "and"
        }
        user = get_user_model().objects.filter(
            username__icontains=form_date["username"])
        response = self.client.get(
            reverse("equipment_information:user-list"),
            form_date)
        self.assertEqual(list(response.context_data["user_list"]),
                         list(user)[:pag])

    def test_forms_search_equipment(self, pag=PAGINATION):
        form_date = {
            "search_query": "as",
        }
        equipment = Equipment.objects.filter(
            Q(name__icontains=form_date["search_query"]) |
            Q(model__icontains=form_date["search_query"]))
        response = self.client.get(
            reverse("equipment_information:equipment-list"),
            form_date)
        self.assertEqual(list(response.context_data["equipment_list"]),
                         list(equipment)[:pag])