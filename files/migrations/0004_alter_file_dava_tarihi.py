# Generated by Django 4.0.6 on 2022-07-31 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_alter_file_dosya'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dava_tarihi',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]
