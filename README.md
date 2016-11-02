# obligatorio_python

Este es el repositorio git para el obligatorio de python 2016 de los integrantes Pablo Perdomo y Manuela Viola. 

Qué hay hecho? 
* Barra de Menu con todos los links para cada CRUD más el buscador que busca acorde al index donde te encuentres (en lugar sería buscador de lugar por nombre, en categoría sera buscador de categoría por nombre, etc). 
* CRUD de Lugar
* CRUD de Categoría
* Esqueleto del resto de los CRUD

Básicamente son todo lo mismo. Ya está todo el proyecto dividido en paquetes por cada clase con sus templates (index y save), url y views y el url de la aplicación ya te redirige al url adecuado. Además todos los index utilizan el mismo paginado que se encuentra en back_end/templates/layout/paginado y para eso no hay que cambiar nada. Basicamente solo se debería cambiar en cada index y save los títulos y campos que corresponan y dentro del views de cada paquete, cambiar la clase Lugar en este caso (porque la estructura fue copiada del paquete Lugar) por la clase adecuada que estamos haciendo y ta todo lo que sea particular de lugar cambiarlo por las particularidades de la clase actual. 


Dejo una página útil para ver los posibles campos para la creación de atributos de las clases en Django:
https://docs.djangoproject.com/es/1.10/ref/models/fields/

Saludos.
