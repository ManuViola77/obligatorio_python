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
    url(r'^categorias', include('back_end.categorias.urls')),
    url(r'^lugares', include('back_end.lugares.urls')),
    url(r'^sectores', include('back_end.sectores.urls')),
    url(r'^asientos', include('back_end.asientos.urls')),
    url(r'^eventos', include('back_end.eventos.urls')),
    url(r'^preciosentradas', include('back_end.preciosentradas.urls')),
    url(r'^entradas', include('back_end.entradas.urls')),
    url(r'^/{0,1}$', views.index),
]
