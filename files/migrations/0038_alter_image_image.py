# Generated by Django 4.1 on 2022-08-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0037_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(max_length=280, upload_to='class'),
        ),
    ]