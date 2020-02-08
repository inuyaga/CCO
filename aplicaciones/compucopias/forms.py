from django import forms
from aplicaciones.compucopias.models import CorreoCco, RegistroEvento

class CorreoForm(forms.ModelForm):
    class Meta:
        model = CorreoCco
        fields = '__all__'
        widgets = {
        'corr_mensaje': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(CorreoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class RegistroEventoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvento
        fields = '__all__'
        widgets = {
        're_direccion_escuela': forms.Textarea(attrs={'rows':2, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistroEventoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
