# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from models import Opcion, Privilegios, Widget


# class OpcionAdmin(admin.ModelAdmin):
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             if not request.POST['propietario']:
#                 obj.propietario = request.user
#         obj.save()


class WidgetAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if not request.POST['propietario']:
                obj.propietario = request.user
            if not request.POST['posicion']:
                obj.posicion = 0
        obj.save()


admin.site.register(Opcion)
admin.site.register(Privilegios)
admin.site.register(Widget)