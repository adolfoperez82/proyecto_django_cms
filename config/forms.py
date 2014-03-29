from django.forms import ModelForm, forms
from config.models import Opcion
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FormularioEdicion(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormularioEdicion, self).__init__(*args, **kwargs)
        from models import Widget

        instance = getattr(self, 'instance', None)
        # if self.instance:
            # self.fields['widget'].queryset = Widget.objects.filter(propietario=self.instance.propietario.id)
            # self.fields['padre'].queryset = Opcion.objects.filter(propietario=self.instance.propietario)

    class Meta:
        model = Opcion
        exclude = ['propietario']

class FormularioCreacion(ModelForm):
    class Meta:
        model = Opcion
        exclude = ['propietario']

class FormularioRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    # def save(self,commit = True):
    #     user = super(FormularioRegistro, self).save(commit = False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user

class FormularioWidget(ModelForm):
    from django.db import models
    from django import forms

    class Meta:
        from models import Widget
        model = Widget
        exclude = ['propietario']

class FormularioNuevoWidget(ModelForm):
    from django.db import models
    class Meta:
        from models import Widget
        model = Widget
        exclude = ['propietario','id']

