# Generated by Django 4.1 on 2022-08-14 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_alter_file_dava_tarihi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dava_tarihi',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]
