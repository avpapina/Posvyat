from django.urls import path
from . import views
from apps.views import RegistrationAPI, TransferAPI, RasselenieAPI

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('main_page/', views.main_page, name='main_page'),
    path('api/v1/registration', RegistrationAPI.as_view(), name='registration'),
    path('api/v1/transfer', TransferAPI.as_view(), name='transfer'),
    path('api/v1/resettlement', RasselenieAPI.as_view(), name = 'resettlement' ),
]
