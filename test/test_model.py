from django.contrib.auth import get_user_model
from django.test import TestCase

from equipment_information.models import Manufacturer, Equipment, EquipmentCategory, Commentary


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} ({manufacturer.country})")

    def test_user_str(self):
        data = {
            "username": "test_driver",
            "password": "Password_test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        user = get_user_model().objects.create(
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        self.assertEqual(str(user),
                         f"{user.username}")

    def test_equipment_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        category = EquipmentCategory.objects.create(
            name="test_equipment_category",
        )
        equipment = Equipment.objects.create(
            name="test_equipment",
            model="test_model_number",
            price=1231.21,
            tech_specifications="""{"test_tech_specifications": "8GB"}""",
            manufacturer=manufacturer,
            category=category,
        )
        self.assertEqual(str(equipment),
                         f"{equipment.manufacturer} "
                         f"{equipment.name} ({equipment.model})")

    def test_commentary_str(self):
        user = get_user_model().objects.create(
            username="test_username",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        equipment = Equipment.objects.create(
            name="test_equipment",
            model="test_model_number",
            price=1231.21,
            tech_specifications="""{"test_tech_specifications": "8GB"}""",
            manufacturer=Manufacturer.objects.create(
                name="test_manufacturer",
                country="test_country",),
            category=EquipmentCategory.objects.create(
                name="test_equipment_category",
            )
        )
        comment = Commentary.objects.create(
            user=user,
            equipment_post=equipment,
            content="test_comment",
        )
        self.assertEqual(str(comment),
                         f"Comment by {comment.user} on {comment.equipment_post}")

    def test_user_favorite_equipment(self):
        equipment = Equipment.objects.create(
            name="test_equipment",
            model="test_model_number",
            price=1231.21,
            tech_specifications="""{"test_tech_specifications": "8GB"}""",
            manufacturer=Manufacturer.objects.create(
                name="test_manufacturer",
                country="test_country", ),
            category=EquipmentCategory.objects.create(
                name="test_equipment_category",
            )
        )
        equipment2 = Equipment.objects.create(
            name="test_equipment2",
            model="test_model_number2",
            price=2231.21,
            tech_specifications="""{"test_tech_specifications2": "8GB2"}""",
            manufacturer=Manufacturer.objects.create(
                name="test_manufacturer2",
                country="test_country2", ),
            category=EquipmentCategory.objects.create(
                name="test_equipment_category2",
            )
        )
        user = get_user_model().objects.create(
            username="test_username",
            password="<PASSWORD>",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        user.favorite_equipment.set([equipment,equipment2])
        self.assertEqual(list(user.favorite_equipment.all()),
                         ([equipment2, equipment]))
