# Generated by Django 4.1 on 2022-08-20 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0019_alter_file_dosya_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='dosya_no',
            field=models.CharField(blank=True, default='', max_length=12),
        ),
    ]
