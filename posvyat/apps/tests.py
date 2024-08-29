from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.models import Registration


class RegistrationAPITestCase(APITestCase):
    def test_registration_creates_entry(self):

        data = {
            "name": "Гей",
            "surname": "геев",
            "middle_name": "геевич",
            "vk": "https://vk.com/gay",
            "tg": "@gay",
            "phone": "+79991234567",
            "university": "ВШЭ",
            "faculty": "ПМИ",
            "group": "БПМИИ666",
            "transfer": "Да, от Одинцово и обратно",
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
