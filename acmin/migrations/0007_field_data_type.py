# Generated by Django 2.1.3 on 2018-12-25 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmin', '0006_auto_20181208_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='data_type',
            field=models.CharField(max_length=10, null=True, verbose_name='数据类型'),
        ),
    ]
