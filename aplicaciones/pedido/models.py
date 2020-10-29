from django.db import models
from django.db.models import FloatField, Sum, F
from django.core.validators import FileExtensionValidator

from django.conf import settings

Usuario = settings.AUTH_USER_MODEL 
STATUS = ((1, 'Creado'), (2, 'Atendiendo'),  (3, 'Surtiendo'), (4, 'En Viaje'), (5, 'Entregado'),)
# 1 CUANDO EL CLIENTE A CREADO EL PEDIDO
# 2 CUANDO UN ASESOR DE VENTA DESCARGUE LA VENTA
# 3 CUANDO ACTUALIZEN NUMERO DE VENTA EN LA TABLA DE COMPRA WEB
# 4 CUANDO ACTUALIZEN NUMERO DE FACTURA
TIPO_DOMICILIO = ((1, 'Trabajo'), (2, 'Casa'),)
TIPO_PAGO = ((1, 'EFECTIVO'),)


class Galeria(models.Model):
    ga_foto=models.ImageField(verbose_name="Imagen", upload_to="img/galeria/")
    ga_alt=models.CharField(verbose_name="Texto alternativo", max_length=150, help_text="Nombre referente a la imagen")
    ga_descripcion=models.CharField(verbose_name="Descripción (opcional)", max_length=250, help_text="Ayuda al SEO", blank=True, null=True)
    def __str__(self):
        return self.ga_alt
    def show_img(self):
        return mark_safe('<img src="{}" style="height: 90px; width: 90px;" alt="{}">'.format(self.ga_foto.url, self.ga_alt))


class Marca(models.Model):
    marca_id_marca = models.AutoField(primary_key=True)
    marca_nombre = models.CharField(max_length=80, verbose_name='Nombre de Marca') 
    marca_logo = models.ImageField(verbose_name="Logo", help_text="Logotipo de la marca", upload_to="img/logos/")
    marca_activar_web=models.BooleanField(verbose_name="Activar en sitio web", help_text="Seleccione si se requiere que sea visible en el sitio", default=False)

    def __str__(self):
        return self.marca_nombre
    
    class Meta:
        ordering = ["marca_nombre"]
        verbose_name_plural = "1. Marcas"


class Area(models.Model):
    area_id_area = models.AutoField(primary_key=True)
    area_nombre = models.CharField(max_length=40, verbose_name='Nombre de area')
    area_activar_promocional = models.BooleanField(verbose_name="Activar promocional en area", default=False)
    area_promocional1 = models.ImageField(verbose_name="Imagen promocional 1", upload_to="img/area/promocional/", help_text="Tamaño sugerido 370px X 200px", null=True, blank=True)
    area_promocional2 = models.ImageField(verbose_name="Imagen promocional 2", upload_to="img/area/promocional/", help_text="Tamaño sugerido 370px X 200px", null=True, blank=True)
    area_icono = models.FileField(verbose_name="Icono png", upload_to="img/area/icono/", validators=[FileExtensionValidator(allowed_extensions=['png'])])
    def __str__(self):
        return self.area_nombre
    class Meta:        
        verbose_name_plural = "2. Areas"

class Subcategoria(models.Model):
    sc_area=models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Area a la que pertenece")
    sc_nombre=models.CharField(max_length=150,verbose_name="Subcategoria")
    def __str__(self):
        return self.sc_nombre
    class Meta:        
        verbose_name_plural = "3. Subcategorias"
class Linea(models.Model):
    l_subcat=models.ForeignKey(Subcategoria, on_delete=models.CASCADE, verbose_name="Subcategoria a la que pertenece")
    l_nombre=models.CharField(max_length=150,verbose_name="Linea") 
    def __str__(self):
        return self.l_nombre
    class Meta:        
        verbose_name_plural = "4. Linea"



class Producto(models.Model):
    producto_codigo = models.CharField(max_length=15, primary_key=True)  
    producto_nombre = models.CharField(max_length=500, verbose_name='Nombre')
    producto_descripcion = models.CharField(max_length=900, verbose_name='Descripcion') 
    producto_imagen = models.ImageField(blank=False, null=False, upload_to="img_productos/", verbose_name='Imagen')
    producto_marca = models.ForeignKey(Marca, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Marca')    
    producto_precio = models.DecimalField('Precio', max_digits=7, decimal_places=2, default=0.00)
    # tipo_producto = models.IntegerField(choices=TIPO_PRODUCTO, null=True, blank=True)
    # producto_es_kit=models.BooleanField(verbose_name='¿Pertenecerá a un Kit?', default=False)
    # producto_kit=models.BooleanField(verbose_name='Kit', default=False)
    # producto_productos=models.ManyToManyField("Producto")
    producto_promocion=models.BooleanField('¿Producto en promoción?', default=False)

    prducto_codigo_barras=models.CharField(max_length=50, verbose_name='Codigo Barras', null=True, blank=True)
    # prducto_localizacion=models.CharField(max_length=50, verbose_name='Localizacion', null=True, blank=True)
    prducto_unidad=models.CharField(max_length=100, verbose_name='Unidad', null=True, blank=True)
    # prducto_resguardo=models.CharField(max_length=50, verbose_name='Localizacion en resguardo', null=True, blank=True)
    prducto_existencia=models.IntegerField(verbose_name='Existencia', null=True, blank=True)

    # producto_descripcion_web=models.TextField('Descripcion enriquecido para sitio web', blank=True, null=True)
    producto_linea=models.ForeignKey(Linea, on_delete=models.CASCADE, verbose_name="Linea", blank=True, null=True)
    producto_fecha_creado=models.DateField(auto_now_add=True)
    producto_galeria=models.ManyToManyField(Galeria, verbose_name="Galeria", help_text="Galeria adicional para sitio web", blank=True)


    class Meta:
        permissions = [
            ('puede_actualizar_precio_volumen', 'Puede actualizar precios de productos en volumen'),
            ]
        ordering = ["producto_nombre"]
        verbose_name_plural = "5. Producto"
     

    def __str__(self):
        return self.producto_codigo

 



class Domicilio(models.Model):
    dom_nom_ap=models.CharField(max_length=130, verbose_name="Nombre y apellido")
    dom_codigo_p=models.IntegerField(verbose_name="Codigo postal")
    dom_estado=models.CharField(max_length=80, verbose_name="Estado")
    dom_delegacion=models.CharField(max_length=80, verbose_name="Delegacion")
    dom_colonia=models.CharField(max_length=200, verbose_name="Colonia / Asentamiento")
    dom_calle=models.CharField(max_length=200, verbose_name="Calle")
    dom_num_ex=models.IntegerField(verbose_name="N° exterior", help_text='Si no tiene un numero escriba 0')
    dom_num_interior=models.IntegerField(verbose_name="N° interior", blank=True, null=True, help_text="Opcional")
    dom_indicaciones=models.CharField(max_length=700, verbose_name="Indicaciones adicionales para entregar tus compras en esta dirección", help_text="Descripción de la fachada, puntos de referencia para encontrarla, indicaciones de seguridad, etc.")
    dom_tipo=models.IntegerField(verbose_name="¿Es tu trabajo o tu casa?", choices=TIPO_DOMICILIO)
    dom_telefono=models.CharField(max_length=10, verbose_name="Telefono de contacto", help_text="Llamarán a este numero si hay algún problema en el envío")
    dom_activo=models.BooleanField(verbose_name="Default dirección")
    dom_creador=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="user_domicilio", verbose_name='Usuario creador', blank=True, null=True)
    def __str__(self):
        return str(self.dom_codigo_p)
    def str_domicilio(self):
        domicilio='C.P:{} calle:{} Colonia:{} N° Exterior:{} N° interior:{},  {}, {}. Recibe: {}, Referencias:{} Tipo:{} Tel:{}'.format(
            self.dom_codigo_p, 
            self.dom_calle, 
            self.dom_colonia, 
            self.dom_num_ex,
            self.dom_num_interior,
            self.dom_delegacion,
            self.dom_estado,
            self.dom_nom_ap,
            self.dom_indicaciones,
            self.get_dom_tipo_display(),
            self.dom_telefono,
            )
        return domicilio


class CompraWeb(models.Model):
    cw_id=models.BigAutoField(primary_key=True)
    cw_fecha = models.DateTimeField(auto_now_add=True)
    cw_cliente=models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name='Cliente')
    cw_status=models.IntegerField(verbose_name="Status compra", choices=STATUS, default=1)
    cw_domicilio=models.ForeignKey(Domicilio, on_delete=models.PROTECT, verbose_name="Domicilio de entrega")
    cw_numero_venta=models.IntegerField(verbose_name="Numero venta", blank=True, null=True)
    cw_numero_factura=models.CharField(max_length=10,verbose_name="Numero factura", blank=True, null=True)
    cw_tipo_pago=models.IntegerField(verbose_name="Forma de pago", choices=TIPO_PAGO, default=1)

    class Meta:
        ordering = ["-cw_fecha"]

    def __str__(self):
        return str(self.cw_id)
    def domicilio(self):
        return self.cw_domicilio.str_domicilio()
    def detalles(self):
        return Detalle_Compra_Web.objects.filter(dcw_pedido_id=self.cw_id)
    def cliente_str(self):
        return "Usuario:{} Cliente:{}".format(self.cw_cliente,self.cw_cliente.rfc)
    def total_compra(self):
        total=Detalle_Compra_Web.objects.filter(dcw_pedido_id=self.cw_id).aggregate(suma_total=Sum(F('dcw_precio') * F('dcw_cantidad'), output_field=FloatField()))['suma_total']
        total=0 if total == None else total
        # total = (total * 0.16) + total
        return round(total, 2)



class Detalle_Compra_Web(models.Model): 
    dcw_pedido_id = models.ForeignKey(CompraWeb, on_delete=models.CASCADE, verbose_name='Numero de compra', blank=True, null=True, related_name='itemsCompras')
    dcw_producto_id = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name='Producto') 
    dcw_cantidad = models.IntegerField(null=True, blank=True, verbose_name='Cantidad')
    dcw_creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT,)
    dcw_precio = models.FloatField(default=0)
    dcw_status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.dcw_pedido_id)
    def sub_total(self):
        subtotal=self.dcw_cantidad*self.dcw_precio
        return subtotal

