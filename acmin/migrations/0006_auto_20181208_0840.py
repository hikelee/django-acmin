# Generated by Django 2.1.3 on 2018-12-08 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmin', '0005_auto_20181207_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='searchable',
            field=models.BooleanField(default=False, verbose_name='可搜索'),
        ),
        migrations.AddField(
            model_name='groupfield',
            name='searchable',
            field=models.BooleanField(default=False, verbose_name='可搜索'),
        ),
        migrations.AddField(
            model_name='userfield',
            name='searchable',
            field=models.BooleanField(default=False, verbose_name='可搜索'),
        ),
    ]
