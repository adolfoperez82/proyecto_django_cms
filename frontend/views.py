# -*- coding: utf-8 -*-
#definiendo codificacion
from __builtin__ import list
from django.shortcuts import render_to_response
from django.template import RequestContext

def Home(request):
    propietario=0
    edicion=False
    # si no hay usuario autenticado, cogera las opciones del admin
    if not request.user.is_authenticated():
        from config.models import Privilegios
        propietario = Privilegios.objects.get(tipo=100).user
        request.session['edicion'] = False
    else:
        propietario = request.user
        edicion=request.session['edicion']

    # hay que buscar la opcion por defecto
    defecto=recuperaOpcionDefecto(propietario)
    request.session['opcionSeleccionada']=defecto
    if request.session.get('edicion',True):
        if not request.session['edicion']==True:
            request.session['edicion']=False
            edicion=request.session['edicion']
    widgets=recuperaWidgets(edicion,propietario,defecto)
    data = {
        'contenido': recuperaContenido(propietario,defecto),
        'posiciones': widgets,
    }
    return render_to_response('home.html',
                              data,
                              context_instance=RequestContext(request),
    )


def cargaPagina(request, opcion_seleccionada):
    from config.models import Opcion
    edicion=False

    if not request.user.is_authenticated():
        from config.models import Privilegios
        propietario = Privilegios.objects.get(tipo=100).user
    else:
        propietario = request.user
    request.session['opcionSeleccionada'] = opcion_seleccionada
    opcion = Opcion.objects.filter(amigable=opcion_seleccionada)
    widgets=recuperaWidgets(edicion,propietario,opcion_seleccionada)
    data = {
        'contenido': recuperaContenido(propietario,opcion_seleccionada),
        'posiciones': widgets,
        'editar': edicion,
    }
    return render_to_response('home.html',
                              data,
                              context_instance=RequestContext(request),
    )


def recuperaWidgets(edicion,user, opcion_seleccionada=None):
    from config.models import Widget, Opcion
    from django.db.models import Count
    widgets=Widget.objects.filter(propietario=user,visible=1).values('posicion').order_by("posicion").annotate(dcount=Count('posicion'))
    posiciones=[]
    for wid in widgets:
        posiciones.append(wid['posicion'])
    bloque=[]
    retorno=[]

    for pos in posiciones:
        widgets = Widget.objects.filter(propietario=user,visible=1,posicion=pos)
        lista_widgets = []
        for wid in widgets:
            bloque=[]
            bloque.append(wid)
            opciones = recuperaOpciones(edicion,opcion_seleccionada,wid)
            bloque.append(opciones)
            lista_widgets.append(bloque)
        bloque={
            "posicion":pos,
            "widgets":lista_widgets
        }
        retorno.append(bloque)
    return retorno

def recuperaOpciones(edicion,opcion_seleccionada,widget,id_padre=None):
    listado=[]
    padres_hijos={}
    from config.models import Opcion
    seleccionada=False
    retorno=""
    if not id_padre:
        opciones=Opcion.objects.filter(padre__isnull=True,widget=widget.id)
    else:
        opciones=Opcion.objects.filter(padre=id_padre,widget=widget.id)
    if opciones:
        clase_ul=""
        if widget.posicion == 2 or widget.posicion == 3:
            clase_ul+="opcion_vertical"
        else:
            clase_ul+="opcion_horizontal"
        if id_padre:
            clase_ul+=" submenu"
        else:
            clase_ul+=" menu"
        retorno+="<ul class='"+clase_ul+"'>"
        for opc in opciones:
            clase=" class='"
            subopciones=Opcion.objects.filter(padre=opc.id)
            if subopciones:
                clase+=" menu"
            if opc.amigable == opcion_seleccionada:
                clase+=" active"
            clase+="'"
            retorno+="<li"+clase+">"
            retorno+="<a href='./pagina="+opc.amigable+"'>"
            retorno+=opc.titulo
            retorno+="</a>"
            if edicion == True:
                retorno+="<a href='/editar="+str(opc.id)+"'>"
                retorno+="<img src='cms/images/editar.png'/>"
                retorno+="</a>"
                retorno+="<a href='/borrar="+str(opc.id)+"'>"
                retorno+="<img src='cms/images/borrar.png'/>"
                retorno+="</a>"
            if subopciones:
                # retorno+="<ul class='submenu'>"
                retorno+=recuperaOpciones(edicion,opcion_seleccionada,widget,opc.id)
                # retorno+="</ul>"
            retorno+="</li>"

        retorno+="</ul>"
    return retorno

def recuperaOpcionDefecto(user):
    from config.models import Widget,Opcion
    retorno = 0
    widgets=Widget.objects.filter(propietario=user,visible=1)
    encontrado=False
    if widgets:
        for wid in widgets:
            opcion=Opcion.objects.filter(widget=wid.id,defecto=1)
            if opcion:
                retorno = opcion[0].amigable
                encontrado=True

        if not encontrado:
            opcion=Opcion.objects.filter(widget=widgets[0].id).order_by("id")
            if opcion:
                retorno = opcion[0].amigable
    # from config.models import Opcion
    # retorno = ""
    # opcion = Opcion.objects.filter(propietario=user,defecto=1)
    # #opcion = Opcion.objects.all()
    # if opcion :
    #     retorno = opcion[0].amigable
    # else:
    #     opcion = Opcion.objects.filter(propietario=user.id).order_by("id")
    #     if(opcion):
    #         retorno = opcion[0].amigable
    #     else:
    #         retorno = 0
    return retorno

def recuperaContenido(user,opcionAmigable=None):
    from config.models import Opcion,Widget
    widgets=Widget.objects.filter(propietario=user)
    retorno = "No existe"
    if widgets:
        for wid in widgets:
            if opcionAmigable:
                opcion=Opcion.objects.filter(amigable=opcionAmigable,widget=wid.id)
            else:
                opcion=Opcion.objects.filter(widget=wid.id)
            if opcion:
                retorno=opcion[0].contenido
    # opcion = Opcion.objects.filter(amigable=opcionAmigable, widget=wid.id)
    # if opcion:
    #     retorno = opcion[0].contenido
    # else:
    #     retorno = "No existe"
    return retorno


def modoEdicion(request):
    from django.http import HttpResponseRedirect
    if request.session.get('edicion') and request.session['edicion'] == True:
        request.session['edicion'] = False
    else:
        request.session['edicion'] = True

    return HttpResponseRedirect("/home")
    # edicion=request.session['edicion']
    # defecto=recuperaOpcionDefecto(request.user.id)
    # widgets=recuperaWidgets(edicion,request.user.id,defecto)
    # propietario=request.user.id
    # data = {
    #     'contenido': recuperaContenido(propietario,defecto),
    #     'posiciones': widgets,
    #     'editar': edicion,
    # }
    # return render_to_response('home.html',
    #                           data,
    #                           context_instance=RequestContext(request),
    # )

def Registro(request):
    from django.http import HttpResponseRedirect
    from config.forms import FormularioRegistro
    from config.models import Privilegios
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)     # create form object
        if form.is_valid():
            obj=form.save()
            user_privs=Privilegios()
            user_privs.user=obj
            user_privs.tipo=5
            obj.save()
            user_privs.save()
            return HttpResponseRedirect("/home")
        else:
            pagina="registro.html"

    data = {
        'form':FormularioRegistro()
    }
    return render_to_response('registro.html',
                              data,
                              context_instance=RequestContext(request),
    )