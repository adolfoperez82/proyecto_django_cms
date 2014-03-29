# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.

class Widget(models.Model):
    OPCION_VISIBLE = (
        (0, "no"),
        (1, "si"),
    )

    POSICION_DEFECTO = (
        (0, "Cabecera derecha"),
        (1, "Cabecera horizontal"),
        (2, "Columna izquierda"),
        (3, "Columna derecha"),
        (4, "Horizontal superior contenido"),
        (5, "Horizontal inferior contenido"),
        (6, "pie"),
    )
    from django.contrib.auth.models import User
    propietario = models.ForeignKey(User, related_name="propietario", null=True, blank=True)
    titulo = models.CharField(max_length=50,blank=False,null=False)
    posicion = models.IntegerField(choices=POSICION_DEFECTO, default=0,blank=False,null=False)
    visible=models.IntegerField(choices=OPCION_VISIBLE, default=1)
    def __str__(self):
        return "%s [propietario: %s]" % (self.titulo.encode('ascii', 'ignore'),self.propietario)

class Opcion(models.Model):
    OPCION_DEFECTO = (
        (0, "no"),
        (1, "si"),
    )
    titulo = models.CharField(max_length=50)
    padre = models.ForeignKey('self',default=0,null=True, blank=True)
    contenido = models.TextField(null=True,blank=True)
    amigable = models.CharField(max_length=50)
    defecto = models.IntegerField(choices=OPCION_DEFECTO, default=0)
    widget =  models.ForeignKey(Widget, related_name="widget")
    class Meta:
        ordering = ['widget']

    def __str__(self):
        return u"[ %s ] -- [ %s > %s ]" % (self.widget.titulo,self.padre, self.titulo)


class Privilegios(models.Model):
    from django.contrib.auth.models import User

    TIPOS = (
        ( 100, 'Admin' ),
        (50, 'Editor' ),
        (10, 'Privilegiado'),
        (5, 'Cliente'),
        (1, 'Activo'),
    )
    user = models.OneToOneField(User, primary_key=True, related_name="user_profile_set")
    tipo = models.IntegerField(max_length=2, choices=TIPOS, default=5)

    def __str__(self):
        retorno = self.user.__getattribute__("username")
        retorno += "("
        if self.tipo == 5:
            retorno += "Alumno"
        if self.tipo == 100:
            retorno += "Admin"
        retorno +=")"
        return retorno


