from rest_framework import serializers

from apps.models import Registration, Transfer, Factions


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class FactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factions
        fields = '__all__'
