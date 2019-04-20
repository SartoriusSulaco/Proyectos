from django.shortcuts import render
from catalogo.models import Libro, Autor, LibroExistente, Editorial, Perfil
from django.contrib.auth.mixins import LoginRequiredMixin #Este sirve para verificar si ha iniciado sesion
from django.views import generic
import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalogo.forms import RenovaciondeLibro

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User

def inicio(request): #Esta es la pagina de inicio, solo realiza un query a la base de datos para mostras las existencia de cada uno

    cantidad_de_libros = Libro.objects.all().count()
    
    cantidad_de_existencias_disponibles = LibroExistente.objects.filter(estado__exact='d').count()

    cantidad_autores = Autor.objects.all().count()
    
    context = {
        'cantidad_de_libros': cantidad_de_libros,
        'cantidad_de_existencias_disponibles': cantidad_de_existencias_disponibles,
        'cantidad_autores': cantidad_autores,
    }
    return render(request, 'inicio.html', context=context)



class ListadoLibros(generic.ListView):  #es el metodo integrado de django para mostrar los listados y los detalles de cada uno de los modelos
    model = Libro
    paginate_by=5

class DetalleLibros(generic.DetailView):
    model = Libro

class ListadoAutores(generic.ListView):
    model = Autor
    paginate_by=5

class DetalleAutores(generic.DetailView):
    model = Autor

class ListadoPerfiles(LoginRequiredMixin,generic.ListView):
    model = Perfil
    paginate_by=5

class DetallePerfiles(LoginRequiredMixin,generic.DetailView):
    model = Perfil






class ListadoPrestamosUsuario(LoginRequiredMixin,generic.ListView): #Lo unico diferente de estos dos metodos a los anteriores es que se realiza un query para filtrar los libros
    model = LibroExistente                                          #prestados, por lo demas se utilizan las vistas integradas de django
    template_name ='catalogo/listadoprestamosusuario.html'
    paginate_by = 5
    
    def get_queryset(self):
        return LibroExistente.objects.filter(prestador=self.request.user).filter(estado__exact='p').order_by('retorno')

class ListadoPrestamosTodo(LoginRequiredMixin, generic.ListView):
    model = LibroExistente
    paginate_by = 5
    def get_queryset(self):
        return LibroExistente.objects.filter(estado__exact='p').order_by('retorno')
    




@permission_required('catalogo.can_mark_returned')  ##Esta definicion es WIP aun no funciona, es para renovar los libros, faltan los formulario de html y el contexto, si no se puede
def Renovacion(request, pk):                        #eliminarlo
    libro_existente = get_object_or_404(LibroExistente, pk=pk)

    if request.method == 'POST':

        form = RenovaciondeLibro(request.POST)
        if form.is_valid():
            libro_existente.retorno = form.cleaned_data['fecharenovacion']
            libro_existente.save()
            return HttpResponseRedirect(reverse('') )

    else:
        nueva_fecharenovacion = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenovaciondeLibro(initial={'fecharenovacion': nueva_fecharenovacion})

    context = {
        'form': form,
        'libro_existente': nueva_fecharenovacion,
    }

    return render(request, 'catalogo/renovacion_de_libro.html', context)



#Vistas genericas para crear, actualizar y eliminar, solo falta probar las de eliminar, y agragar los permisos para que solo los administradores puedan hacerlos
#Por el momento solo el superusuario lo puede realizar

class AutorCrear(LoginRequiredMixin ,CreateView):
    model = Autor
    fields = '__all__'

class AutorActualizar(LoginRequiredMixin ,UpdateView):
    model = Autor
    fields = '__all__'

class AutorEliminar(LoginRequiredMixin ,DeleteView):
    model = Autor

class LibroCrear(LoginRequiredMixin ,CreateView):
    model = Libro
    fields = '__all__'

class LibroActualizar(LoginRequiredMixin ,UpdateView):
    model = Libro
    fields = '__all__'

class LibroEliminar(LoginRequiredMixin ,DeleteView):
    model = Libro


class PerfilCrear(LoginRequiredMixin, CreateView):
    model= Perfil
    fields='__all__'
    login_required = True
    permission_required ='catalog.administrador'

class PerfilActualizar(LoginRequiredMixin ,UpdateView):
    model = Perfil
    fields = ['nombre','correo','edad','fotografia']


class UsuarioCrear(LoginRequiredMixin, CreateView):
    model= User
    fields='__all__'
    login_required = True
    permission_required ='catalog.administrador'