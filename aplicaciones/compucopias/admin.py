from django.contrib import admin
from aplicaciones.compucopias.models import Evento, Marca, CorreoCco, Departamento
# Register your models here.

class ConfigCorreos(admin.ModelAdmin):
    list_display = ('corr_nombre', 
                    'corr_email',
                    'corr_telefono',
                    'corr_asunto',
                    'corr_mensaje',
                    'corr_depo',
                    'corr_crado',)
    list_filter = ['corr_depo', 'corr_crado']


admin.site.register(Departamento)
admin.site.register(Evento)
admin.site.register(Marca)
admin.site.register(CorreoCco, ConfigCorreos) 