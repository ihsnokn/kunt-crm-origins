# Generated by Django 4.1 on 2022-08-18 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0011_alter_file_dosya_durumu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dosya_no',
            field=models.CharField(max_length=12),
        ),
    ]
