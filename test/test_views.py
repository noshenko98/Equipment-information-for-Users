from django.test import TestCase, Client
from django.urls import reverse


class PublicFormatTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        response_index = self.client.get(reverse("equipment_information:index"))
        response_manufacturer = self.client.get(reverse("equipment_information:manufacturer-list"))
        response_equipment_category = self.client.get(reverse("equipment_information:equipments-category-list"))
        response_user = self.client.get(reverse("equipment_information:user-list"))
        response_equipment = self.client.get(reverse("equipment_information:equipment-list"))
        self.assertNotEqual(response_index.status_code, 200)
        self.assertNotEqual(response_manufacturer.status_code, 200)
        self.assertNotEqual(response_equipment_category.status_code, 200)
        self.assertNotEqual(response_user.status_code, 200)
        self.assertNotEqual(response_equipment.status_code, 200)