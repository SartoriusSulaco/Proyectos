# Generated by Django 2.1.7 on 2019-04-21 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0008_auto_20190421_0432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'ordering': ['usuario'], 'permissions': (('es_administrador', 'Administrador'), ('es_usuario_comun', 'Usuario Comun'))},
        ),
    ]
