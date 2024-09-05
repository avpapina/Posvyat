import os

from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response

from apps.models import Registration, Transfer, Rasselenie, Factions

from apps.serializers import RegistrationSerializer, TransferSerializer, RasselenieSerializer, FactionsSerializer

from apps.supportfunc import read_json_choices, check_phone

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
        
        response = check_phone(phone)
        if(response < 0):
            return Response(
                {"error": "Phones file not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        elif(response == 0):
            return Response(
                    {"error": "Phone number not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class FactionsAPI(generics.CreateAPIView):
    serializer_class = FactionsSerializer
    queryset = Factions.objects.all()

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        priority = set()
        for i in range(6):
            priority.add(request.data.get('priority'+str(i+1)))
        if(len(priority) >= 6):

            if not phone:
                return Response(
                    {"error": "Phone are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            response = check_phone(phone)
            if(response < 0):
                return Response(
                    {"error": "Phones file not found."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif(response == 0):
                return Response(
                        {"error": "Phone number not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                        {"error": "You have the same priorities"},
                        status=status.HTTP_404_NOT_FOUND
                    )


class RasselenieAPI(generics.CreateAPIView):
    serializer_class = RasselenieSerializer
    queryset = Rasselenie.objects.all()

    def create(self, request, *args, **kwargs):

        fields = ['name', 'surname', 'middle_name', 'vk', 'tg', 'program', 'group', 'course']

        for field in fields:
            datas = request.data.get(field)

            if not datas:
                return Response(
                    {"error": f"{field} field are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        file_path = os.path.join(
            os.path.dirname(__file__),
            'phones.txt'
        )

        phone = request.data.get('phone')

        if not phone:
            return Response(
                {"error": "This field are required."},
                status=status.HTTP_400_BAD_REQUEST
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
