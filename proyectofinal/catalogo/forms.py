import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalogo.models import Perfil
from django.contrib.auth.models import User
from django.forms import ModelForm


class RenovaciondeLibro(forms.Form):   #Es un formulacion para la renovacion de los libros, todavia es WIP
    fecharenovacion = forms.DateField(help_text="Ingrese una fecha")

    def clean_renewal_date(self):
        data = self.cleaned_data['fecharenovacion']
        if data < datetime.date.today():
            raise ValidationError(_('Fecha Invalida'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha invalida, es mas de un mes'))
        return data

