# Generated migration to replace CloudinaryField with ImageField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0008_configuracionsitio'),
    ]

    operations = [
        # ImagenProducto.imagen: CloudinaryField -> ImageField
        migrations.AlterField(
            model_name='imagenproducto',
            name='imagen',
            field=models.ImageField(upload_to='productos/', verbose_name='imagen'),
        ),
        # ImagenSeccion.imagen: CloudinaryField -> ImageField
        migrations.AlterField(
            model_name='imagenseccion',
            name='imagen',
            field=models.ImageField(upload_to='secciones/', verbose_name='imagen'),
        ),
        # HeroHome.imagen_fondo: CloudinaryField -> ImageField
        migrations.AlterField(
            model_name='herohome',
            name='imagen_fondo',
            field=models.ImageField(blank=True, help_text='Imagen de fondo del hero', null=True, upload_to='hero/', verbose_name='imagen_fondo'),
        ),
        # HeroHome.logo: CloudinaryField -> ImageField
        migrations.AlterField(
            model_name='herohome',
            name='logo',
            field=models.ImageField(blank=True, help_text='Logo de la marca', null=True, upload_to='logo/', verbose_name='logo'),
        ),
        # GaleriaTrabajo.imagen: CloudinaryField -> ImageField
        migrations.AlterField(
            model_name='galeriatrabajo',
            name='imagen',
            field=models.ImageField(upload_to='galeria/', verbose_name='imagen'),
        ),
    ]

