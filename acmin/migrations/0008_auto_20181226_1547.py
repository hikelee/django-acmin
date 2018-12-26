# Generated by Django 2.1.4 on 2018-12-26 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmin', '0007_auto_20181226_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupfield',
            name='help_text',
            field=models.TextField(null=True, verbose_name='帮助文本'),
        ),
        migrations.AddField(
            model_name='groupfield',
            name='max_length',
            field=models.IntegerField(null=True, verbose_name='最大长度'),
        ),
        migrations.AddField(
            model_name='groupfield',
            name='serialize',
            field=models.BooleanField(null=True, verbose_name='可序列化'),
        ),
        migrations.AddField(
            model_name='userfield',
            name='help_text',
            field=models.TextField(null=True, verbose_name='帮助文本'),
        ),
        migrations.AddField(
            model_name='userfield',
            name='max_length',
            field=models.IntegerField(null=True, verbose_name='最大长度'),
        ),
        migrations.AddField(
            model_name='userfield',
            name='serialize',
            field=models.BooleanField(null=True, verbose_name='可序列化'),
        ),
    ]