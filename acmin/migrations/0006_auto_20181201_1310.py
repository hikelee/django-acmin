# Generated by Django 2.1.3 on 2018-12-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmin', '0005_superpermissionmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superpermissionmodel',
            options={'ordering': ['-id'], 'verbose_name': '超級模型', 'verbose_name_plural': '超級模型'},
        ),
        migrations.AlterField(
            model_name='grouppermission',
            name='enabled',
            field=models.BooleanField(db_index=True, default=True, verbose_name='开通'),
        ),
        migrations.AlterField(
            model_name='userpermission',
            name='enabled',
            field=models.BooleanField(db_index=True, default=True, verbose_name='开通'),
        ),
        migrations.AlterUniqueTogether(
            name='grouppermission',
            unique_together={('group', 'model')},
        ),
        migrations.AlterUniqueTogether(
            name='userpermission',
            unique_together={('user', 'model')},
        ),
    ]
