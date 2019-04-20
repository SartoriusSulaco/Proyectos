from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('libros/', views.ListadoLibros.as_view(), name='libros'),
    path('libros/<int:pk>', views.DetalleLibros.as_view(), name='libro-detalle'),
    path('autores/', views.ListadoAutores.as_view(), name='autores'),
    path('autores/<int:pk>', views.DetalleAutores.as_view(), name='autor-detalle'),
    path('perfiles/', views.ListadoPerfiles.as_view(), name='perfiles'),
    path('perfiles/<int:pk>', views.DetallePerfiles.as_view(), name='perfil-detalle'),  #Estos url solo son para observar los datos de la biblioteca, los perfiles solo los pueden ver los
                                                                                        #administradores
]

urlpatterns += [   
    path('mislibros/', views.ListadoPrestamosUsuario.as_view(), name='mis-prestamos'), #url para ver los libros prestados
    path(r'librosprestados/' , views.ListadoPrestamosTodo.as_view(),name='prestamos')  #Modificar esto, por el momento si funciona, pero verificar que significa el r
]

urlpatterns += [   
    path('libros/<uuid:pk>/renovacion/', views.Renovacion, name='Renovacion'), #Este url todavia es WIP
]

urlpatterns += [  
    path('autores/crear/', views.AutorCrear.as_view(), name='autor_crear'),  #Faltan agregar los url de eliminar para todos, probar bien el url usuario crear
    path('autores/<int:pk>/actualizar/', views.AutorActualizar.as_view(), name='autor_actualizar'),
    path('autores/<int:pk>/eliminar/', views.AutorEliminar.as_view(), name='autor_eliminar'),
    path('libros/crear/', views.LibroCrear.as_view(), name='libro_crear'),
    path('libros/<int:pk>/actualizar/', views.LibroActualizar.as_view(), name='libro_actualizar'),
    path('libros/<int:pk>/eliminar/', views.LibroEliminar.as_view(), name='libro_eliminar'),
    path('perfiles/crear/', views.PerfilCrear.as_view(), name='perfiles_crear'),
    path('perfiles/<int:pk>/actualizar/', views.PerfilActualizar.as_view(), name='perfiles_actualizar'),
    path('usuario/crear/', views.UsuarioCrear.as_view(), name='usuario_crear'),
]
