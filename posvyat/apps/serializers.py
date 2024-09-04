from rest_framework import serializers

from apps.models import Registration, Transfer, Rasselenie


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class RasselenieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rasselenie
        fields = '__all__'