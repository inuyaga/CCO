from django.db import models

class Galeria(models.Model):
    imagen = models.ImageField(upload_to='headers', null=True, blank=True)
 
    def __str__(self):
        return str(self.imagen)