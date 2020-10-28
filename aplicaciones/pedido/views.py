from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

import json

from django.contrib.auth.models import User
from aplicaciones.pedido.models import Area, Producto, Detalle_Compra_Web, CompraWeb
from aplicaciones.pedido.serializers import *

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import F

class AutenticacionUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)       
        serializerUser = UserSerializer(user) 
        data = {
            'token': token.key,             
            'usuario':serializerUser.data,
        }
        return Response(data)


class RegistracionUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    permission_classes = (AllowAny, )
    lookup_field = 'id'


class UsuarioInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]        
    def get(self, request):        
        serializerUser = UserInfoSerializer(request.user)        
        return Response(serializerUser.data)

class AreaViewApp(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
        
    def get(self, request):
        area = Area.objects.all()
        serializerArea = AreaSerializer(area, many=True, context={'request': request}) 
        content = {
            'area': serializerArea.data,            
            }
        return Response(content)
class ProductosItems(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
        
    def get(self, request):
        print(request.user.is_authenticated)
        productos = Producto.objects.filter(producto_promocion=True)[:20]
        if request.user.is_authenticated:
            serializer = ProductoSerializer(productos, many=True, context={'request': request}) 
        else:
            serializer = ProductoSerializerExclude(productos, many=True, context={'request': request}) 
        
                
        return Response(serializer.data)


class ProductosItemsFilterTipiado(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
        
    def get(self, request):
        busqueda = request.GET.get('search')
        productos = Producto.objects.filter(producto_nombre__icontains=busqueda)
        
        if request.user.is_authenticated:
            serializer = ProductoSerializer(productos, many=True, context={'request': request}) 
        else:
            serializer = ProductoSerializerExclude(productos, many=True, context={'request': request}) 
            
        return Response(serializer.data)

class ProductosItemsFilterArea(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
        
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.filter(producto_linea__l_subcat__sc_area=self.kwargs.get('pk'))
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            serializer = ProductoSerializer(productos, many=True, context={'request': request}) 
        else:
            serializer = ProductoSerializerExclude(productos, many=True, context={'request': request}) 

        return Response(serializer.data)





class NotificacionConteoCompra(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
        
    def get(self, request):
        area = Area.objects.all()
        serializerArea = AreaSerializer(area, many=True, context={'request': request}) 
        content = {
            'area': serializerArea.data,            
            }
        return Response(content)

class DomicilioCreate(generics.CreateAPIView):
    queryset = Domicilio.objects.all()
    serializer_class = DomicilioSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):                
        request.data._mutable = True
        request.data['dom_creador']=request.user.id
                
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Detalle_Compra_WebCreate(generics.CreateAPIView):    
    serializer_class = Detalle_Compra_WebCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):                
        request.data._mutable = True        
        porducto = Producto.objects.get(producto_codigo=request.data['dcw_producto_id'])

        try:
            Detalle_Compra_Web.objects.get(dcw_producto_id=request.data['dcw_producto_id'], dcw_status=False, dcw_creado_por=request.user)  
            Detalle_Compra_Web.objects.filter(dcw_producto_id=request.data['dcw_producto_id'], dcw_status=False, dcw_creado_por=request.user).update(dcw_cantidad=F('dcw_cantidad')+request.data['dcw_cantidad'])              
            return Response({}, status=status.HTTP_201_CREATED)       
        except ObjectDoesNotExist as error:            
            request.data['dcw_creado_por']=request.user.id
            request.data['dcw_precio']=porducto.producto_precio        
                    
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class ConteoCarShops(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]        
    def get(self, request):        
        conteo_pre_compra = Detalle_Compra_Web.objects.filter(dcw_status=False, dcw_creado_por=request.user).count()
        data = {
            'conteo_pre_compra':conteo_pre_compra
        }
        return Response(data)

class Detalle_Compra_WebView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]        
    def get(self, request):        
        pre_compra = Detalle_Compra_Web.objects.filter(dcw_status=False, dcw_creado_por=request.user)
        
        serializer = Detalle_Compra_WebSerializer(pre_compra, many=True, context={'request': request})
        
        return Response(serializer.data)



class DeleteDetalle_CompraWebView(generics.DestroyAPIView):
    queryset = Detalle_Compra_Web
    serializer_class = Detalle_Compra_WebCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "id"




class DomicilioView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]        
    def get(self, request):        
        domicilios = Domicilio.objects.filter(dom_creador=request.user)        
        serializer = DomicilioSerializer(domicilios, many=True, context={'request': request})        
        return Response(serializer.data)



class DomicilioActivoUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]        
    def get(self, request):        
        domicilios = Domicilio.objects.filter(dom_creador=request.user, dom_activo=True)        
        serializer = DomicilioSerializer(domicilios, many=True, context={'request': request})        
        return Response(serializer.data)


class DomicilioUpdateUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]       
    queryset =  Domicilio.objects.all()
    serializer_class = DomicilioUpdateSerializer 
    
    def update(self, request, *args, **kwargs):
        Domicilio.objects.filter(dom_creador=request.user).update(dom_activo=False)  
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class DomicilioUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]       
    queryset =  Domicilio.objects.all()
    serializer_class = DomicilioSerializer 
    
    # def update(self, request, *args, **kwargs):
    #     Domicilio.objects.filter(dom_creador=request.user).update(dom_activo=False)  
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    


class FinalizarCompraView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    def post(self, request):
        cw=CompraWeb(
            cw_cliente=request.user,
            cw_domicilio_id=request.data['IDomicilio'],
        )
        cw.save()
        Detalle_Compra_Web.objects.filter(dcw_status=False, dcw_creado_por=request.user).update(dcw_status=True, dcw_pedido_id=cw.cw_id)
        content = {
            'idCompraWeb':cw.cw_id
        }
        return Response(content, status=status.HTTP_201_CREATED)