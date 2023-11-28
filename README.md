# Q - System
## Planteamiento del problema
### Ejercicio # 1

- Crear una lista del Objeto Persona (dni, appPaterno, appMatterno) y deberás ordenar la lista por DNI y de ahí por apellido paterno, pintando la lista desordenada y de ahí ordenada. La información debe ser obtenida por una pequeña base de datos con estos tres datos. Incluya las sentencias en SQL para poder obtener los datos y la integración para obtener la consulta.

### Ejercicio # 2 

- Se requiere la construcción de un REST API, que transmita la lista del Objeto Persona.  

### Ejercicio #3

- Es necesario implementar la función de consulta a través de una aplicación tercera para poder asegurar que toda la prueba está corriendo adecuadamente. 
- Para poder probarlo, es importante que pueda existir al menos una llamada usando herramientas terceras como el SOAP UI


# Instalación y Configuración Inicial
## Clonar el Repositorio

```
git clone https://github.com/AlexanderAndreChavezCabana/qsystem-api.git
cd tu-repositorio
```
## Crear y Activar el Entorno Virtual
```
python3.10 -m venv venv
source venv/bin/activate
```
## Instalar Dependencias del Proyecto
```
pip install -r requirements.txt
```

## Ingresar a la carpeta del proyecto, aplicar  migraciones y correr el sistema
```
cd app
# De ser necesario aplicar migraciones, en este caso el proyecto y base de datos se subieron completo para las pruebas respectivas
python manage.py makemigrations
python manage.py migrate

# Correr el sistema
python manage.py runserver
```

# Ejercicios Resueltos
## Ejercicio #1: Crear y Ordenar Lista de Personas

### *models.py*
```
#models.py
from django.db import models

# Models Persona
class Persona(models.Model):
    dni = models.CharField(max_length=10)
    appPaterno = models.CharField(max_length=255)
    appMaterno = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dni} - {self.appPaterno} {self.appMaterno}"
    
    class Meta:
        ordering = ['-created_at']
```
#### Captura models.py
![](imagenes_doc/models.png)


#### Consultas SQL para listas
```
# Obtener la Lista Desordenada
SELECT * FROM api.persona;

# Obtener la Lista Ordenada por DNI, Apellido Paterno y Apellido Materno
SELECT * FROM api.persona ORDER BY dni, appPaterno, appMaterno;
```

## Ejercicio #2: Construcción de REST API
### *serializers.py*
```
# serializers.py
from rest_framework import serializers
from .models import Persona

# Serializer Persona
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
```

#### Captura serializers.py
![](imagenes_doc/serializers.png)

### *urls.py*
```
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# View Set Persona
from api.views import PersonaViewSet

router = ExtendedSimpleRouter()

router.register(r'personas', PersonaViewSet, basename='persona')

urlpatterns = [
    path('', include(router.urls)),

    # Rutas adicionales
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
```

#### Captura urls.py
![](imagenes_doc/urls.png)

### *views.py*
```
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import PersonaViewSet

# En lugar de usar DefaultRouter, utiliza ExtendedSimpleRouter
router = ExtendedSimpleRouter()

# Registra la vista PersonaViewSet con el router
router.register(r'personas', PersonaViewSet, basename='persona')

urlpatterns = [
    # Rutas generadas por el router extendido
    path('', include(router.urls)),

    # Rutas adicionales
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
```

#### Captura views.py
![](imagenes_doc/views.png)


### Ver Swagger UI:
Abre tu navegador web y ve a la siguiente dirección: http://127.0.0.1:8000/api/schema/swagger/#/

Esto debería abrir el Swagger UI, donde podrás ver la documentación interactiva de tu API y probar los endpoints directamente desde la interfaz de usuario.

#### Captura de Pantalla de Swagger UI
- Swagger UI mostrando la documentación de la API:

![](imagenes_doc/swagger.png)

### Generar Token:

1. Dirigete hasta la sección "Token" y haz clic en "Try it out!".
![Token](imagenes_doc/token.png)
2. Llena los parámetros requeridos, en este caso con las credenciales *{ "username": "chavez", "password": "chavez" }* y ejecuta:
![Token Obtain](imagenes_doc/token1.png)


   #### Captura de pantalla: Token Obtenido
   ![Token execute](imagenes_doc/token_obtenido.png)

### Realizar una Solicitud con Token:

1. Utiliza el token obtenido para realizar solicitudes a recursos protegidos.
    #### Utilizar token en Swagger
    1. Dirigete hasta la parte superior y presiona en authorize e inserta el token mostrada en la imagen anterior (en tu caso se mostrará otro token, inserta el obtenido).
    ![Token](imagenes_doc/insertar_token.png)


    2. Puedes hacerlo utilizando la operación dirigiendote a la `get personas` bajo la sección "personas".

   #### Captura de pantalla: Solicitud con Token
   ![Solicitud con Token](imagenes_doc/obtener_lista_personas.png)
