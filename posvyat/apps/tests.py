import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.models import Registration, Transfer


class RegistrationAPITestCase(APITestCase):
    def test_registration_creates_entry(self):
        data = {
            "name": "Сидел",
            "surname": "Втюрьме",
            "middle_name": "Дуров",
            "vk": "https://vk.com/sad",
            "tg": "@goodluck",
            "phone": "+79991234567",
            "bday": "2003-12-25",
            "sex": "Женский",
            "university": "ВШЭ",
            "faculty": "ПМИ",
            "group": "БПМИИ666",
            "transfer": "Да, от Парка Победы и обратно",
            "course": 1,
            "health_features": "Нет особых требований"
        }

        url = reverse('registration')

        response = self.client.post(
            url,
            data,
            format='json',
            headers={
                'Content-Type': 'application/json'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Registration.objects.count(), 1)

        registration = Registration.objects.first()
        self.assertEqual(registration.name, data['name'])
        self.assertEqual(registration.surname, data['surname'])
        self.assertEqual(registration.tg, data['tg'])
        self.assertEqual(registration.phone, data['phone'])


class TransferAPITests(APITestCase):
    def setUp(self):
        print(f"Current directory: {os.getcwd()}")
        self.phone_file_path = 'apps/phones.txt'
        try:
            with open(self.phone_file_path, 'w', encoding='utf-8') as f:
                f.write('+79999999999\n')
                f.write('+79991234568\n')
        except Exception as e:
            print(f"Error creating phone file: {e}")
        assert os.path.exists(self.phone_file_path), "Phone file was not created."

        self.url = reverse('transfer')

    def tearDown(self):
        import os
        if os.path.exists(self.phone_file_path):
            os.remove(self.phone_file_path)

    def test_create_transfer_with_valid_phone(self):
        data = {
            "name": "Дима",
            "surname": "Димов",
            "middle_name": "Димович",
            "email": "dao@diydx.ru",
            "vk": "https://vk.com/dimov",
            "tg": "@dimov",
            "phone": "+79991234568",
            "_from": "Парк Победы",
            "departure_time": "15:15"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Transfer.objects.filter(phone=data['phone']).exists())

    def test_create_transfer_with_invalid_phone(self):
        data = {
            "name": "Дима",
            "surname": "Димов",
            "middle_name": "Димович",
            "email": "dao@diydx.ru",
            "vk": "https://vk.com/dimov",
            "tg": "@dimov",
            "phone": "+79987788778",
            "_from": "Парк Победы",
            "departure_time": "15:30"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Phone number not found."})

    def test_create_transfer_without_phone(self):
        data = {
            "name": "Дима",
            "surname": "Димов",
            "middle_name": "Димович",
            "email": "dao@diydx.ru",
            "vk": "https://vk.com/dimov",
            "tg": "@dimov",
            "_from": "Парк Победы",
            "departure_time": "15:30"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Phone are required."})

    def test_create_transfer_with_missing_phone_file(self):
        self.tearDown()
        data = {
            "name": "Дима",
            "surname": "Димов",
            "middle_name": "Димович",
            "email": "dao@diydx.ru",
            "vk": "https://vk.com/dimov",
            "tg": "@dimov",
            "phone": "+79991234568",
            "_from": "Парк Победы",
            "departure_time": "15:30"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "Phones file not found."})
