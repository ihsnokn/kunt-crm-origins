# Generated by Django 4.1 on 2022-08-29 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0023_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='class'),
        ),
    ]