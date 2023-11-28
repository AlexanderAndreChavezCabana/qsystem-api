from django.shortcuts import render
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.db.models import F

from .serializers import PersonaSerializer
from .models import Persona

@extend_schema_view(
    list=extend_schema(description='Permite obtener una lista de personas.'),
    retrieve=extend_schema(description='Permite obtener una persona.'),
    create=extend_schema(description='Permite crear una persona.'),
    update=extend_schema(description='Permite actualizar una persona.'),
    destroy=extend_schema(description='Permite eliminar una persona')
)
class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', 'created_at')
        fields = [field.strip() for field in ordering.split(',')]
        initial_queryset = Persona.objects.order_by(*fields)

        dni = self.request.query_params.get('dni')
        app_paterno = self.request.query_params.get('appPaterno')
        app_materno = self.request.query_params.get('appMaterno')

        if dni:
            initial_queryset = initial_queryset.filter(dni=dni)

        if app_paterno:
            initial_queryset = initial_queryset.filter(appPaterno=app_paterno)

        if app_materno:
            initial_queryset = initial_queryset.filter(appMaterno=app_materno)

        if 'created_at' in fields:
            initial_queryset = initial_queryset.order_by(F('created_at').desc(), *fields)

        return initial_queryset
    
    