# Generated by Django 4.1 on 2022-08-20 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0020_alter_file_dosya_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='dosya_notu',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
