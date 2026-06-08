from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from equipment_information.models import Manufacturer, Equipment, Commentary, EquipmentCategory, User


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


class PrivateFormatTests(TestCase):
    fixtures = ["equipment_data.json"]
    PAGINATION = 5

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_test",
            password="<PASSWORD1234>",
        )
        self.client.force_login(self.user)

    def test_private_format(self):
        response_index = self.client.get(reverse("equipment_information:index"))
        response_manufacturer = self.client.get(reverse("equipment_information:manufacturer-list"))
        response_equipment_category = self.client.get(reverse("equipment_information:equipments-category-list"))
        response_user = self.client.get(reverse("equipment_information:user-list"))
        response_equipment = self.client.get(reverse("equipment_information:equipment-list"))
        self.assertEqual(response_index.status_code, 200)
        self.assertEqual(response_manufacturer.status_code, 200)
        self.assertEqual(response_equipment_category.status_code, 200)
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(response_equipment.status_code, 200)

    def test_context_index(self):
        count_manufacturers = Manufacturer.objects.all().count()
        count_equipments = Equipment.objects.all().count()
        count_comments = Commentary.objects.all().count()
        response_index = self.client.get(reverse("equipment_information:index"))
        self.assertEqual(response_index.context["num_manufacturers"], count_manufacturers)
        self.assertEqual(response_index.context["num_equipments"], count_equipments)
        self.assertEqual(response_index.context["num_comments"], count_comments)


    def test_context_manufacturer(self, pag=PAGINATION):
        manufacturer = Manufacturer.objects.all()
        response_manufacturer = self.client.get(reverse("equipment_information:manufacturer-list"))
        self.assertEqual(list(response_manufacturer.context["manufacturer_list"]),
                         list(manufacturer)[:pag])

    def test_equipment_category(self, pag=PAGINATION):
        count_equipments_category = EquipmentCategory.objects.all()
        response_equipment_category = self.client.get(reverse("equipment_information:equipments-category-list"))
        self.assertEqual(list(response_equipment_category.context["equipment_category_list"]),list(count_equipments_category)[:pag])


    def test_user(self, pag=PAGINATION):
        user_list = User.objects.all()
        response_user = self.client.get(reverse("equipment_information:user-list"))
        self.assertEqual(list(response_user.context["user_list"]),list(user_list)[:pag])

    def test_equipment(self, pag=PAGINATION):
        equipment = Equipment.objects.all()
        response_equipment = self.client.get(reverse("equipment_information:equipment-list"))
        self.assertEqual(list(response_equipment.context["equipment_list"]),list(equipment)[:pag])