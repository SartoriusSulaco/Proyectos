from django.contrib import admin
from catalogo.models import Autor, Editorial, Libro, LibroExistente, Perfil

admin.site.register(Editorial)
admin.site.register(Perfil)   #Registra los modelos Editorial y Perfil

class AutorAdmin(admin.ModelAdmin):  #Esta clase es para ordenar el modelo autor en la vista de administracion
    list_display = ('apellido', 'nombre')
    fields = ['apellido', 'nombre']

admin.site.register(Autor, AutorAdmin)  #Registra el modelo


class LibroExistenteInline(admin.TabularInline):
    model = LibroExistente

@admin.register(Libro)
class BookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editorial')  #forma de desplegar el modelo Libro
    inlines = [LibroExistenteInline]

@admin.register(LibroExistente)
class LibroExistenteAdmin(admin.ModelAdmin):  
    list_display = ('libro', 'estado', 'prestador', 'retorno', 'id')  #Forma de desplegar el modelo libro existente, tambien incluye filtros para mejorar la busqueda
    list_filter = ('estado', 'retorno')
    
    fieldsets = (
        (None, {
            'fields': ('libro', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('estado', 'retorno','prestador')
        }),
    )
