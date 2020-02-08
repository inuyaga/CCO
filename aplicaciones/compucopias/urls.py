from django.urls import path
from aplicaciones.compucopias import views

app_name='compucopias'

urlpatterns = [
    path('', views.index.as_view(), name='inicio'),
    path('registro/evento/maestros/', views.RegistroEvento.as_view(), name='registro'),
]