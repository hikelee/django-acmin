# Generated by Django 2.1.3 on 2018-12-01 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creatable', models.BooleanField(default=True, verbose_name='可创建')),
                ('savable', models.BooleanField(default=True, verbose_name='可保存')),
                ('removable', models.BooleanField(default=True, verbose_name='可删除')),
                ('cloneable', models.BooleanField(default=True, verbose_name='可复制')),
                ('exportable', models.BooleanField(default=True, verbose_name='可导出')),
                ('viewable', models.BooleanField(default=True, verbose_name='可查看')),
                ('listable', models.BooleanField(default=True, verbose_name='可列表')),
                ('enabled', models.BooleanField(default=True, verbose_name='开通')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '用户组权限',
                'verbose_name_plural': '用户组权限',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creatable', models.BooleanField(default=True, verbose_name='可创建')),
                ('savable', models.BooleanField(default=True, verbose_name='可保存')),
                ('removable', models.BooleanField(default=True, verbose_name='可删除')),
                ('cloneable', models.BooleanField(default=True, verbose_name='可复制')),
                ('exportable', models.BooleanField(default=True, verbose_name='可导出')),
                ('viewable', models.BooleanField(default=True, verbose_name='可查看')),
                ('listable', models.BooleanField(default=True, verbose_name='可列表')),
                ('enabled', models.BooleanField(default=True, verbose_name='开通')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户权限',
                'verbose_name_plural': '用户权限',
                'ordering': ['-id'],
            },
        ),
    ]