from django.db import models

class Departamento(models.Model):
    dp_nombre=models.CharField('Nombre Departamento',  max_length=100)
    def __str__(self):
        return self.dp_nombre
class CorreoCco(models.Model):
    corr_nombre=models.CharField('Nombre',  max_length=200)
    corr_email=models.EmailField('Email',max_length=300)
    corr_telefono=models.CharField('Número teléfonico',max_length=10)
    corr_asunto=models.CharField('Asunto',max_length=150)
    corr_mensaje=models.CharField('Escriba aqui su mensaje',max_length=700)
    corr_depo=models.ForeignKey(Departamento, on_delete=models.PROTECT, verbose_name='Departamento al que se dirige', blank=False, null=True)
    corr_crado=models.DateTimeField(verbose_name='Creado', auto_now_add=True)

    def __str__(self):
        return self.corr_email
    class Meta:
        verbose_name = "Correos de contacto"

class Evento(models.Model):
    event_nombre=models.CharField('Nombre del evento',  max_length=350)
    event_imagen=models.ImageField('Imagen promocional del evento', upload_to='imgEventos/')
    event_fecha_inicial=models.DateField('Fecha inicial del evento')
    event_fecha_final=models.DateField('Fecha final del evento')
    event_ubicacion=models.CharField('Direccion del evento',  max_length=800)
    event_hora_inicio=models.TimeField('Hora de inicio')
    event_hora_fin=models.TimeField('Hora de fianlización')
    event_patrocinado=models.CharField('Patrocinado por', max_length=800)
    event_especificacion=models.CharField('Especificaciones adicionales', max_length=250)
    def __str__(self):
        return self.event_nombre

class Marca(models.Model):
    marca_nombre=models.CharField('Nombre Marca', max_length=100)
    marca_img=models.ImageField('Imagen', upload_to='marca_img/')
    def __str__(self):
        return self.marca_nombre




 
