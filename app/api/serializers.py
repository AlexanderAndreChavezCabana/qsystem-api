# serializers.py
from rest_framework import serializers
from .models import Persona

# Serializer Persona
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
