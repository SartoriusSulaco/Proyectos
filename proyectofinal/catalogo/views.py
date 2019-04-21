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
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from axes.models import CommonAccess, AccessAttempt


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

class ListadoPerfiles(PermissionRequiredMixin,generic.ListView):
    model = Perfil
    permission_required='catalogo.crear_usuarios'
    paginate_by=5

class DetallePerfiles(PermissionRequiredMixin,generic.DetailView):
    model = Perfil
    permission_required='catalogo.crear_usuarios'







class ListadoPrestamosUsuario(LoginRequiredMixin,generic.ListView): #Lo unico diferente de estos dos metodos a los anteriores es que se realiza un query para filtrar los libros
    model = LibroExistente                                          #prestados, por lo demas se utilizan las vistas integradas de django
    template_name ='catalogo/listadoprestamosusuario.html'
    paginate_by = 5
    
    def get_queryset(self):
        return LibroExistente.objects.filter(prestador=self.request.user).filter(estado__exact='p').order_by('retorno')

class ListadoPrestamosTodo(PermissionRequiredMixin, generic.ListView):
    model = LibroExistente
    permission_required='catalogo.crear_usuarios'
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

class AutorCrear(PermissionRequiredMixin ,CreateView):
    model = Autor
    permission_required='catalogo.crear_usuarios'
    fields = '__all__'

class AutorActualizar(PermissionRequiredMixin ,UpdateView):
    model = Autor
    permission_required='catalogo.crear_usuarios'
    fields = '__all__'

class AutorEliminar(PermissionRequiredMixin ,DeleteView):
    model = Autor
    permission_required='catalogo.crear_usuarios'
    success_url = reverse_lazy('autores')

class LibroCrear(PermissionRequiredMixin ,CreateView):
    model = Libro
    permission_required='catalogo.crear_usuarios'
    fields = '__all__'

class LibroActualizar(PermissionRequiredMixin ,UpdateView):
    model = Libro
    permission_required='catalogo.crear_usuarios'
    fields = '__all__'

class LibroEliminar(PermissionRequiredMixin ,DeleteView):
    model = Libro
    permission_required='catalogo.crear_usuarios'
    success_url = reverse_lazy('libros')


class PerfilCrear(PermissionRequiredMixin, CreateView):
    model= Perfil
    permission_required='catalogo.crear_usuarios'
    fields='__all__'
    login_required = True
 

class PerfilActualizar(PermissionRequiredMixin ,UpdateView):
    model = Perfil
    permission_required='catalogo.crear_usuarios'
    fields = ['nombre','correo','edad','fotografia']

class PerfilEliminar(PermissionRequiredMixin , DeleteView):
    model = Perfil
    permission_required='catalogo.crear_usuarios'
    success_url = reverse_lazy('perfiles')


class UsuarioCrear(PermissionRequiredMixin, CreateView):
    model= User
    permission_required='catalogo.crear_usuarios'
    fields=['username','password','passwordconfirmation']
    login_required = True
    success_url = reverse_lazy('inicio')

from django.contrib import messages
from django.shortcuts import redirect

@permission_required('catalogo.crear_usuarios')
def UsuarioC(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'El usuario ha sido creado exitosamente')
            return redirect('registrar')
 
    else:
        f = UserCreationForm()
 
    return render(request, 'catalogo/registrar.html', {'form': f})