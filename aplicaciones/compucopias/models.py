from django.db import models
SE_ENTERO=(
        (1, 'SITIO WEB'),
        (2, 'SUCURSAL'),
        (3, 'REDES SOCIALES'),
        (4, 'ANUNCIO'),
        (5, 'OTRO'),
        )
NO_PARTICIPACION=((1, 'NO'), (2, 'SI'))
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


class RegistroEvento(models.Model):
    re_id=models.BigAutoField(primary_key=True)
    re_sede=models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name='Sede', blank=False, null=True)
    re_question_participacion=models.IntegerField(verbose_name="¿Primera participacion?", choices=NO_PARTICIPACION)
    re_q_como_se_entero=models.IntegerField(choices=SE_ENTERO, verbose_name="¿Como se enteró del evento?")
    re_nombre=models.CharField(max_length=150, verbose_name="Nombre completo")
    re_telefono=models.CharField(max_length=10, verbose_name="Numero de telefono")
    re_email=models.EmailField(verbose_name="Correo Electronico")
    re_nombre_escuela=models.CharField(max_length=250, verbose_name="Nombre de la escuela")
    re_direccion_escuela=models.CharField(max_length=300, verbose_name="Direccion de escuela")
    def __str__(self):
        return "{} {}".format(self.re_nombre, self.re_sede)

    def save(self, *args, **kwargs):
        self.re_nombre = (self.re_nombre).upper()
        self.re_nombre_escuela = (self.re_nombre_escuela).upper()
        self.re_direccion_escuela = (self.re_direccion_escuela).upper()
        return super(RegistroEvento, self).save(*args, **kwargs)
