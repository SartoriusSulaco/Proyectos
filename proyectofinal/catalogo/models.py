from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse 
import uuid #para identificar las copias existentes
from django.db.models.signals import post_save
from django.dispatch import receiver


class Editorial(models.Model):  #Solo es un modelo para ingresar diferentes editoriales
    nombre = models.CharField(max_length=200, help_text='Ingresa una editorial')
    
    def __str__(self):
        return self.nombre



class Libro(models.Model): #Es el modelo de libros, ForeigKey porque es una relacion uno a varios
    isbn = models.CharField('ISBN', max_length=13)
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    editorial = models.ForeignKey('Editorial', on_delete=models.SET_NULL, null=True)
    edicion = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)

    TIPO_CUBIERTA = (
        ('d', 'Dura'),
        ('b', 'Blanda'),
    )

    cubierta = models.CharField(
        max_length=1,
        choices=TIPO_CUBIERTA,
        blank=True,
        default='d',
    )

    paginas = models.CharField(max_length=200)

    ESTANTERIA_LETRA = (
        ('x', 'Estanteria A'),
        ('y', 'Estanteria B'),
        ('z', 'Estanteria C'),
    )

    estanteria = models.CharField(
        max_length=1,
        choices=ESTANTERIA_LETRA,
        blank=True,
        default='x',
    )

    comentario = models.TextField(max_length=1000, help_text='Ingrese la synopsis del libro')
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self): #esta definicion es para redireccionar con los url y la pk
        return reverse('libro-detalle', args=[str(self.id)])



class LibroExistente(models.Model): #Este modelo crea instancia de la clase libro, con un ID unico para cada libro en especial, por ello se pueden crear varias
                                    #copias del mismo libro y trabajar cada copia por separado
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID para esta copia del libro')
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True) 
    retorno = models.DateField(null=True, blank=True)
    prestador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    ESTADO_LIBRO = (
        ('p', 'Prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_LIBRO,
        blank=True,
        default='d',
    )

    @property
    def atrasado(self):  #Esta propiedad es para elevar las sanciones si no regresa el libro a tiempo
        if self.retorno and date.today() > self.retorno:
            return True
        return False

    class Meta:
        ordering = ['retorno']

    def __str__(self):
        return '{0} ({1})'.format(self.id,self.libro.titulo)


class Autor(models.Model):  #Un modelo para autor, este puede poseer muchos libros
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def librosdeautor(self):        #Esta definicion es para filtrar los libros que pertenecen a un autor en especifico
        Libro.objects.filter(autor=self).values_list('titulo',flat=True)

    class Meta:  #Estos permisos son para retornar libros, todavia son WIP
        ordering = ['nombre', 'apellido']
        permissions = (("can_mark_returned", "Set book as returned"),) 

    def get_absolute_url(self): #Definicion para redireccionar los url
        return reverse('autor-detalle', args=[str(self.id)])

    def __str__(self):
        return '{0},{1}'.format(self.apellido,self.nombre)



class Perfil(models.Model): #Este modelo agranda el auth de django agregandole mas opciones
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=254)
    edad = models.CharField(max_length=3)
    fotografia = models.ImageField(null=True, blank=True, upload_to ='perfiles')#Todavia falta verificar la fotografia y ver la direccion en donde se guarda, agregarla a base_generic.html
                                                                                #para que se muestre en la pagina de inicio


    class Meta:  #Todavia es WIP, django no actualiza los permisos
        ordering = ['usuario']
        permissions = (("es_administrador", "usuario_comun"),) 

    def get_absolute_url(self): #Sirve para redireccionar el URL
        return reverse('perfil-detalle', args=[str(self.id)])


@receiver(post_save, sender=User)   #Estos metodos sirven para actualizar el modelo perfil cuando se modifique el modelo USER de django
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def save_user_perfil(sender, instance, **kwargs):
    instance.perfil.save()
