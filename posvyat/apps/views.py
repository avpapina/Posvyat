from django.shortcuts import render, redirect
from rest_framework import generics

from apps.models import Registration


def main_page(request):
    return render(request, 'main_page.html')


def start_page(request):
    return redirect('main_page')


class RegistrationAPI(generics.CreateAPIView):
    queryset = Registration.objects.all()
