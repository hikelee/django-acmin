# Generated by Django 2.1.3 on 2018-12-06 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'ordering': ['id'], 'verbose_name': '地区', 'verbose_name_plural': '地区'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['id'], 'verbose_name': '城市', 'verbose_name_plural': '城市'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ['id'], 'verbose_name': '省份', 'verbose_name_plural': '省份'},
        ),
    ]
