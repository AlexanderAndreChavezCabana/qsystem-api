from django.db import models

# Create your models here.

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
