# Generated by Django 4.1 on 2022-08-30 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0035_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='dosya_notu',
        ),
    ]
