# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def Widgets(request):
    from config.models import Widget
    from config.forms import FormularioWidget
    lista = []
    msg = ""
    if request.method == "POST":
        if 'guardar' in request.POST:
            widget_id = request.POST['id']
            obj = Widget.objects.get(pk=widget_id, propietario=request.user.id)
            form = FormularioWidget(request.POST, instance=obj)
            if form.is_valid():
                msg = "Guardado correctamente"
            form.save()
        elif 'borrar' in request.POST:
            widget_id = request.POST['id']
            msg = borraWidget(widget_id, request.user.id)
        elif 'nuevo' in request.POST:
            from config.forms import FormularioNuevoWidget
            form = FormularioNuevoWidget(request.POST)
            if form.is_valid():
                opt = form.save(commit=False)
                opt.propietario = request.user
                opt.save()
                msg = "Guardado correctamente"
            else:
                msg = "Ha habido un error"
        else:
            msg = "Ha habido un error"

    widgets = Widget.objects.filter(propietario=request.user.id).order_by("posicion")
    if widgets:
        for wid in widgets:
            parejas={
                "id":wid.id,
                "formulario":FormularioWidget(instance=wid),
            }
            lista.append(parejas)
            pagina = 'widgets.html'

    else:
        lista = 0
        pagina = 'widgets.html'
    nuevo = FormularioWidget()
    data = {
        "nuevo": nuevo,
        "lista_widgets": lista,
        "msg": msg,
        "edicion": 1,
    }
    return render_to_response(pagina,
                              data,
                              context_instance=RequestContext(request),
    )


def borraWidget(widget_id, user_id):
    from config.models import Opcion, Widget

    opciones = Opcion.objects.filter(widget=widget_id)
    retorno = ""
    if opciones:
        retorno = "El Widget no está vacio"
    else:
        Widget.objects.filter(id=widget_id, propietario=user_id).delete()
        retorno = "Borrado correctamente"
    return retorno


def creaOpcion(request):
    from config.forms import FormularioCreacion
    from config.models import Opcion, Widget

    msg = ""
    if request.method == "POST":
        form = FormularioCreacion(request.POST)
        if form.is_valid():
            if request.POST['defecto'] == '1':
                widgets=Widget.objects.filter(propietario=request.user.id)
                for wid in widgets:
                    Opcion.objects.filter(widget=wid.id).update(defecto=0)
            opt = form.save(commit=False)
            opt.save()
            msg = "Guardado correctamente"
        else:
            msg = "Ha habido un error"
    else:
        usuario = request.user
        form = FormularioCreacion()
        form.fields['widget'].queryset = Widget.objects.filter(propietario=request.user).order_by('titulo')
        # form.fields['padre'].queryset = Opcion.objects.filter(propietario=request.user).order_by('widget')
    data = {
        'msg': msg,
        'form': form,
    }
    return render_to_response('opcion.html',
                              data,
                              context_instance=RequestContext(request),
    )


def editaOpcion(request, id_opcion):
    from config.forms import FormularioEdicion
    from config.models import Opcion,Widget
    form=0
    msg = ""
    if request.method == "POST":
        form_bbdd = Opcion.objects.get(pk=id_opcion)
        form = FormularioEdicion(request.POST, instance=form_bbdd)
        if form.is_valid():
            if request.POST['defecto'] == '1':
                widgets=Widget.objects.filter(propietario=request.user.id)
                for wid in widgets:
                    opcion = Opcion.objects.filter(widget=wid.id).update(defecto=0)
            form.save()
            msg = "Guardado correctamente"
        else:
            msg = "Ha habido un error"
    else:
        encontrado=False
        widgets=Widget.objects.filter(propietario=request.user.id).values("id")
        opcion = Opcion.objects.get(pk=id_opcion)
        for wid in widgets:
            print opcion.widget
            print wid['id']
            if opcion.widget.id == wid['id']:
                encontrado=True
                form = FormularioEdicion(instance=opcion)
        if not encontrado:
            form = 0
            msg = "No existe"
    data = {
        'msg': msg,
        'form': form,
        'edicion':1,
    }
    return render_to_response('opcion.html',
                              data,
                              context_instance=RequestContext(request),
    )

def borraOpcion(request, id_opcion):
    from django.http import HttpResponseRedirect
    from config.forms import FormularioEdicion
    from config.models import Opcion,Widget
    pagina="opcion.html"
    msg = ""
    form=0
    if request.method == "POST":
        widgets=Widget.objects.filter(propietario=request.user.id)
        encontrada=False
        for wid in widgets:
            opcion=Opcion.objects.filter(pk=id_opcion,widget=wid.id)[0]
            if opcion:
                encontrada=True
                form=FormularioEdicion(instance=opcion)
        form = FormularioEdicion(request.POST, instance=opcion)
        if form.is_valid() and encontrada:
            Opcion.objects.filter(id=id_opcion).delete()
            return HttpResponseRedirect("/home")
        else:
            msg = "Ha habido un error"
            pagina='opcion.html'

        if form.is_valid():
            Opcion.objects.filter(id=id_opcion).delete()
            return HttpResponseRedirect("/home")
        else:
            msg = "Ha habido un error"
            pagina='opcion.html'
    else:
        widgets=Widget.objects.filter(propietario=request.user.id)
        encontrada=False
        for wid in widgets:
            opcion=Opcion.objects.filter(pk=id_opcion,widget=wid.id)[0]
            if opcion:
                encontrada=True
                form=FormularioEdicion(instance=opcion)
        if not encontrada:
            msg="No existe"

    data = {
        'msg': msg,
        'form': form,
        'borrar':True,
        # 'borrar':True,
    }
    return render_to_response(pagina,
                              data,
                              context_instance=RequestContext(request),
    )
