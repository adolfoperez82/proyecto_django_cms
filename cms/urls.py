from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'frontend.views.Home', name='home'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^modoEdicion',"frontend.views.modoEdicion", name="modoEdicion"),
    url(r'^creaOpcion',"backend.views.creaOpcion", name="creaOpcion"),
    url(r'^login', 'django.contrib.auth.views.login',{'template_name': 'login.html'},name='login'),
    url(r'^registro', 'frontend.views.Registro',name='registro'),
    url(r'^widgets', 'backend.views.Widgets',name='widgets'),
    url(r'^logout','django.contrib.auth.views.logout',{'next_page': '/home'}),
    url(r'^home','frontend.views.Home',name="home"),
    url(r'^editar=(?P<id_opcion>\w+)', 'backend.views.editaOpcion',name="editaOpcion"),
    url(r'^borrar=(?P<id_opcion>\w+)', 'backend.views.borraOpcion',name="borraOpcion"),
    # Uncomment the next line to enable the admin:
    url(r'pagina=(?P<opcion_seleccionada>\w+)', 'frontend.views.cargaPagina', name='contenido_opcion'),
)
