
from django.urls import path, include
from aplicaciones.pedido import views as PedidoView



urlpatterns = [
    path('v1/login/', PedidoView.AutenticacionUser.as_view(), name='index'),
    path('v1/registrer/', PedidoView.RegistracionUser.as_view(), name='registrar'),
    path('v1/userinfo/', PedidoView.UsuarioInfoView.as_view(), name='info'),
    path('v1/userinfo/update/<int:id>/', PedidoView.UpdateUserView.as_view(), name='up_user'),
    path('v1/page/inicial/', PedidoView.AreaViewApp.as_view(), name='inicial_page'),
    path('v1/productos/lista/', PedidoView.ProductosItems.as_view(), name='prod'),
    path('v1/productos/lista/filtro/<int:pk>/', PedidoView.ProductosItemsFilterArea.as_view(), name='prod_find'),
    path('v1/productos/lista/filtro/', PedidoView.ProductosItemsFilterTipiado.as_view(), name='prod_find_tipe'),
    path('v1/domicilio/crear/', PedidoView.DomicilioCreate.as_view(), name='domicilio_crear'),
    path('v1/add/shop/car/', PedidoView.Detalle_Compra_WebCreate.as_view(), name='car_shop_add'),
    path('v1/cnteo/shop/car/', PedidoView.ConteoCarShops.as_view(), name='car_shop_count'),
    path('v1/shop/car/', PedidoView.Detalle_Compra_WebView.as_view(), name='car_shop'),
    path('v1/shop/car/delete/<int:id>/', PedidoView.DeleteDetalle_CompraWebView.as_view(), name='car_shop_delete'),
    path('v1/domicilios/get/user/', PedidoView.DomicilioView.as_view(), name='domicilios'),
    path('v1/domicilio/get/user/activo/', PedidoView.DomicilioActivoUserView.as_view(), name='domicilio_activo'),
    path('v1/domicilio/update/user/<int:pk>/', PedidoView.DomicilioUpdateUserView.as_view(), name='domicilio_update'),
    path('v1/domicilio/update/<int:pk>/', PedidoView.DomicilioUpdateView.as_view(), name='domicilio_update_v'),
    path('v1/finalizar/compra/', PedidoView.FinalizarCompraView.as_view(), name='end_compra'),
    
]