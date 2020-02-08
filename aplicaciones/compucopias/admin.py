from django.contrib import admin
from aplicaciones.compucopias.models import Evento, Marca, CorreoCco, Departamento, RegistroEvento
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

class ConfigRegistroEvento(admin.ModelAdmin):
    list_display = (
                    're_nombre',
                    're_sede', 
                    're_question_participacion',
                    're_q_como_se_entero',
                    're_telefono',
                    're_email',
                    're_nombre_escuela',
                    're_direccion_escuela',)
    list_filter = ['re_sede', 're_question_participacion', 're_q_como_se_entero']


admin.site.register(Departamento)
admin.site.register(Evento)
admin.site.register(Marca)
admin.site.register(CorreoCco, ConfigCorreos) 
admin.site.register(RegistroEvento, ConfigRegistroEvento) 