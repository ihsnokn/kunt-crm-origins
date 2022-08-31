# Generated by Django 4.0.6 on 2022-07-31 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_alter_file_dava_tarihi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='dosya',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='class')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.file')),
            ],
        ),
    ]