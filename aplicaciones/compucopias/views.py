from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from aplicaciones.galeria.models import Galeria
from aplicaciones.compucopias.forms import CorreoForm, RegistroEventoForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from aplicaciones.compucopias.models import Evento, Marca, RegistroEvento

class index(TemplateView):
    template_name = "compucopias/base.html"
    def get_context_data(self, **kwargs): 
        context = super(index, self).get_context_data(**kwargs)
        context['galeria_list'] = Galeria.objects.all()
        context['form_correo'] = CorreoForm()
        context['even_nombre'] = Evento.objects.all()
        context['marca_list'] = Marca.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        form = CorreoForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje guardado correctamente')
        else:
            messages.warning(request, 'Error al guardar')
        url=reverse('compucopias:inicio')
        return redirect(url)


class RegistroEvento(CreateView):
    model = RegistroEvento
    form_class = RegistroEventoForm
    template_name = "compucopias/registro.html"
    success_url = reverse_lazy('compucopias:inicio')

    