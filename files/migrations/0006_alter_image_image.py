# Generated by Django 4.0.6 on 2022-07-31 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_remove_file_dosya_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='class'),
        ),
    ]
