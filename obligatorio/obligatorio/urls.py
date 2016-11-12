"""obligatorio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from back_end import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^back_end/categorias', include('back_end.categorias.urls')),
    url(r'^back_end/lugares', include('back_end.lugares.urls')),
    url(r'^back_end/sectores', include('back_end.sectores.urls')),
    url(r'^back_end/asientos', include('back_end.asientos.urls')),
    url(r'^back_end/eventos', include('back_end.eventos.urls')),
    url(r'^back_end/preciosentradas', include('back_end.preciosentradas.urls')),
    url(r'^back_end/entradas', include('back_end.entradas.urls')),
    url(r'^back_end/{0,1}$', views.index),
    url(r'^back_end/signin/{0,1}$', views.signin),
    url(r'^back_end/signout/{0,1}$', views.signout),
    url(r'^back_end/registrar/{0,1}$', views.registrar),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
