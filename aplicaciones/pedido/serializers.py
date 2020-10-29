
from rest_framework import serializers
from aplicaciones.pedido.models import Producto, Area, Subcategoria, Linea, Domicilio, Detalle_Compra_Web, CompraWeb

from django.contrib.auth.models import User
from django.utils.formats import localize



class DomicilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilio
        fields = [
            'id', 
            'dom_nom_ap',
            'dom_codigo_p',
            'dom_estado',
            'dom_delegacion',
            'dom_colonia',
            'dom_calle',
            'dom_num_ex',
            'dom_num_interior',
            'dom_indicaciones',
            'dom_tipo',
            'dom_telefono',
            'dom_activo',
            'dom_creador',
            'str_domicilio',
            ]
class DomicilioUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilio
        fields = ['dom_activo',]


class HoraFormat1n8(serializers.RelatedField):
    def to_representation(self, value):
        hora = localize(value)
        return hora


class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    date_joined = HoraFormat1n8(read_only=True)
    last_login = HoraFormat1n8(read_only=True)
    # user_domicilio = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']
class UserInfoSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    date_joined = HoraFormat1n8(read_only=True)
    last_login = HoraFormat1n8(read_only=True)
    user_domicilio = DomicilioSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'user_domicilio']
class UserEditSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    date_joined = HoraFormat1n8(read_only=True)
    last_login = HoraFormat1n8(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AreaSerializer(serializers.ModelSerializer):
    # subcategoria_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = Area
        fields = '__all__'
class SubcategoriaSerializer(serializers.ModelSerializer):
    sc_area = AreaSerializer()
    class Meta:
        model = Subcategoria
        fields = '__all__'
class LineaSerializer(serializers.ModelSerializer):
    l_subcat = SubcategoriaSerializer(many=False, read_only=True)
    class Meta:
        model = Linea
        fields = '__all__'
class ProductoSerializer(serializers.ModelSerializer):
    producto_marca = serializers.StringRelatedField()
    producto_linea = LineaSerializer(many=False, read_only=True)   
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoSerializerExclude(serializers.ModelSerializer):
    producto_marca = serializers.StringRelatedField()
    producto_linea = LineaSerializer(many=False, read_only=True)   
    class Meta:
        model = Producto
        exclude = ('producto_precio', )




class Detalle_Compra_WebSerializer(serializers.ModelSerializer):
    dcw_producto_id=ProductoSerializer(many=False)
    class Meta:
        model = Detalle_Compra_Web
        fields = [
            'id', 
            'dcw_pedido_id', 
            'dcw_producto_id', 
            'dcw_cantidad', 
            'dcw_creado_por', 
            'dcw_precio', 
            'dcw_status', 
            'sub_total', 
            ]

class Detalle_Compra_WebCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Detalle_Compra_Web
        fields = '__all__'


class MisComprasSerializer(serializers.ModelSerializer):
    cw_domicilio = DomicilioSerializer()
    cw_fecha = HoraFormat1n8(read_only=True)
    cw_status = serializers.CharField(source='get_cw_status_display')
    cw_tipo_pago = serializers.CharField(source='get_cw_tipo_pago_display')
    cw_cliente = serializers.StringRelatedField()
    itemsCompras = Detalle_Compra_WebSerializer(many=True)
    class Meta:
        model = CompraWeb
        fields = [
            'cw_id',
            'cw_fecha',
            'cw_cliente',
            'cw_status',
            'cw_domicilio',
            'cw_numero_venta',
            'cw_numero_factura',
            'cw_tipo_pago',
            'total_compra',
            'itemsCompras'
        ]