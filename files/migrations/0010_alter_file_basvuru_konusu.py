# Generated by Django 4.1 on 2022-08-18 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0009_alter_file_lawyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='basvuru_konusu',
            field=models.CharField(choices=[('hasar', 'Hasar'), ('hasar_imms', 'Hasar Imms'), ('deger_kaybi', 'Değer Kaybı'), ('deger_kaybi_imms', 'Değer Kaybı Imms'), ('hasar_ve_deger_kaybi', 'Hasar ve Değer Kaybı'), ('maluliyet', 'Maluliyet'), ('destekten_yoksun_kalma', 'Destekten Yoksun Kalma'), ('odeme_bekleyen', 'Ödeme Bekleyen'), ('diger', 'Diğer')], default='', max_length=100),
        ),
    ]
