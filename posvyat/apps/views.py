import os

from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response

from apps.models import Registration, Transfer

from apps.serializers import RegistrationSerializer, TransferSerializer


def main_page(request):
    return render(request, 'main_page.html')


def start_page(request):
    return redirect('main_page')


class RegistrationAPI(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class TransferAPI(generics.CreateAPIView):
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')

        if not phone:
            return Response(
                {"error": "Phone are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Файл с телефонами пусть будет в одной дирректории с views.py
        file_path = os.path.join(
            os.path.dirname(__file__),
            'phones.txt'
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                phones = file.read().splitlines()
                if phone in phones:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {"error": "Phone number not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
        except FileNotFoundError:
            return Response(
                {"error": "Phones file not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
