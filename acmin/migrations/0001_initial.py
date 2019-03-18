# Generated by Django 2.1.3 on 2019-03-18 18:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('title', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='值')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
            ],
            options={
                'verbose_name': '选项',
                'verbose_name_plural': '选项',
                'ordering': ['field', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='名称')),
                ('value', models.TextField(verbose_name='值')),
            ],
            options={
                'verbose_name': '配置',
                'verbose_name_plural': '配置',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=100, verbose_name='描述')),
                ('sequence', models.IntegerField(default=100, verbose_name='排序')),
                ('app', models.CharField(max_length=100, verbose_name='应用')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
            ],
            options={
                'verbose_name': '模型',
                'verbose_name_plural': '模型',
                'ordering': ['sequence', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=200, verbose_name='显示名称')),
                ('sequence', models.IntegerField(verbose_name='序号')),
                ('listable', models.BooleanField(default=True, verbose_name='在列表中显示')),
                ('formable', models.BooleanField(default=True, verbose_name='在表单中显示')),
                ('sortable', models.BooleanField(default=True, verbose_name='可排序')),
                ('exportable', models.BooleanField(default=True, verbose_name='可导出')),
                ('nullable', models.BooleanField(default=False, verbose_name='可以为空')),
                ('unique', models.BooleanField(default=False, verbose_name='是否唯一性')),
                ('default', models.CharField(blank=True, max_length=500, null=True, verbose_name='默认值')),
                ('editable', models.BooleanField(default=True, verbose_name='可编辑')),
                ('searchable', models.BooleanField(default=False, verbose_name='可搜索')),
                ('filterable', models.BooleanField(default=True, verbose_name='可过滤')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='帮助文本')),
                ('attribute', models.CharField(max_length=100, verbose_name='字段名称')),
                ('group_sequence', models.IntegerField(verbose_name='分组序号')),
                ('python_type', models.CharField(max_length=200, verbose_name='原生类型')),
                ('data_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='数据类型')),
                ('max_length', models.IntegerField(blank=True, null=True, verbose_name='最大长度')),
                ('serialize', models.BooleanField(blank=True, null=True, verbose_name='可序列化')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base', to='acmin.ContentType', verbose_name='模型')),
                ('contenttype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contenttype', to='acmin.ContentType', verbose_name='字段模型')),
            ],
            options={
                'verbose_name': '字段',
                'verbose_name_plural': '字段',
                'ordering': ['base', 'group_sequence', 'sequence'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GroupConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='名称')),
                ('value', models.TextField(verbose_name='值')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '配置(用户组)',
                'verbose_name_plural': '配置(用户组)',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GroupContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=100, verbose_name='描述')),
                ('sequence', models.IntegerField(default=100, verbose_name='排序')),
                ('app', models.CharField(max_length=100, verbose_name='应用')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '模型(用户组)',
                'verbose_name_plural': '模型(用户组)',
                'ordering': ['group', 'sequence'],
            },
        ),
        migrations.CreateModel(
            name='GroupField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=200, verbose_name='显示名称')),
                ('sequence', models.IntegerField(verbose_name='序号')),
                ('listable', models.BooleanField(default=True, verbose_name='在列表中显示')),
                ('formable', models.BooleanField(default=True, verbose_name='在表单中显示')),
                ('sortable', models.BooleanField(default=True, verbose_name='可排序')),
                ('exportable', models.BooleanField(default=True, verbose_name='可导出')),
                ('nullable', models.BooleanField(default=False, verbose_name='可以为空')),
                ('unique', models.BooleanField(default=False, verbose_name='是否唯一性')),
                ('default', models.CharField(blank=True, max_length=500, null=True, verbose_name='默认值')),
                ('editable', models.BooleanField(default=True, verbose_name='可编辑')),
                ('searchable', models.BooleanField(default=False, verbose_name='可搜索')),
                ('filterable', models.BooleanField(default=True, verbose_name='可过滤')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='帮助文本')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Field', verbose_name='默认字段')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '字段(用户组)',
                'verbose_name_plural': '字段(用户组)',
                'ordering': ['group', 'field'],
            },
        ),
        migrations.CreateModel(
            name='GroupFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='过滤器名称')),
                ('value_type', models.SmallIntegerField(choices=[(10, '固定值'), (5, '请求属性')], verbose_name='值类型')),
                ('attribute', models.CharField(max_length=100, verbose_name='属性名')),
                ('value', models.CharField(max_length=500, verbose_name='属性值')),
                ('enabled', models.BooleanField(default=True, verbose_name='开通')),
                ('contenttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.ContentType')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '过滤器(用户组)',
                'verbose_name_plural': '过滤器(用户组)',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('creatable', models.BooleanField(default=False, verbose_name='可创建')),
                ('savable', models.BooleanField(default=False, verbose_name='可保存')),
                ('removable', models.BooleanField(default=False, verbose_name='可删除')),
                ('cloneable', models.BooleanField(default=False, verbose_name='可复制')),
                ('exportable', models.BooleanField(default=False, verbose_name='可导出')),
                ('viewable', models.BooleanField(default=False, verbose_name='可查看')),
                ('listable', models.BooleanField(default=False, verbose_name='可列表')),
                ('selectable', models.BooleanField(default=True, verbose_name='可选择')),
                ('contenttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.ContentType')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group')),
            ],
            options={
                'verbose_name': '权限(用户组)',
                'verbose_name_plural': '权限(用户组)',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SuperPermissionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '超級模型',
                'verbose_name_plural': '超級模型',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='名称')),
                ('value', models.TextField(verbose_name='值')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '配置(用户)',
                'verbose_name_plural': '配置(用户)',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=100, verbose_name='描述')),
                ('sequence', models.IntegerField(default=100, verbose_name='排序')),
                ('app', models.CharField(max_length=100, verbose_name='应用')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '模型(用户)',
                'verbose_name_plural': '模型(用户)',
                'ordering': ['user', 'sequence'],
            },
        ),
        migrations.CreateModel(
            name='UserField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verbose_name', models.CharField(max_length=200, verbose_name='显示名称')),
                ('sequence', models.IntegerField(verbose_name='序号')),
                ('listable', models.BooleanField(default=True, verbose_name='在列表中显示')),
                ('formable', models.BooleanField(default=True, verbose_name='在表单中显示')),
                ('sortable', models.BooleanField(default=True, verbose_name='可排序')),
                ('exportable', models.BooleanField(default=True, verbose_name='可导出')),
                ('nullable', models.BooleanField(default=False, verbose_name='可以为空')),
                ('unique', models.BooleanField(default=False, verbose_name='是否唯一性')),
                ('default', models.CharField(blank=True, max_length=500, null=True, verbose_name='默认值')),
                ('editable', models.BooleanField(default=True, verbose_name='可编辑')),
                ('searchable', models.BooleanField(default=False, verbose_name='可搜索')),
                ('filterable', models.BooleanField(default=True, verbose_name='可过滤')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='帮助文本')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Field')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '字段(用户)',
                'verbose_name_plural': '字段(用户)',
                'ordering': ['user', 'field'],
            },
        ),
        migrations.CreateModel(
            name='UserFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='过滤器名称')),
                ('value_type', models.SmallIntegerField(choices=[(10, '固定值'), (5, '请求属性')], verbose_name='值类型')),
                ('attribute', models.CharField(max_length=100, verbose_name='属性名')),
                ('value', models.CharField(max_length=500, verbose_name='属性值')),
                ('enabled', models.BooleanField(default=True, verbose_name='开通')),
                ('contenttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '过滤器(用户)',
                'verbose_name_plural': '过滤器(用户)',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('creatable', models.BooleanField(default=False, verbose_name='可创建')),
                ('savable', models.BooleanField(default=False, verbose_name='可保存')),
                ('removable', models.BooleanField(default=False, verbose_name='可删除')),
                ('cloneable', models.BooleanField(default=False, verbose_name='可复制')),
                ('exportable', models.BooleanField(default=False, verbose_name='可导出')),
                ('viewable', models.BooleanField(default=False, verbose_name='可查看')),
                ('listable', models.BooleanField(default=False, verbose_name='可列表')),
                ('selectable', models.BooleanField(default=True, verbose_name='可选择')),
                ('contenttype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '权限(用户)',
                'verbose_name_plural': '权限(用户)',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='contenttype',
            unique_together={('app', 'name')},
        ),
        migrations.AddField(
            model_name='choice',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Field', verbose_name='默认字段'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acmin.Group'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='userpermission',
            unique_together={('user', 'contenttype')},
        ),
        migrations.AlterUniqueTogether(
            name='userfield',
            unique_together={('user', 'field')},
        ),
        migrations.AlterUniqueTogether(
            name='usercontenttype',
            unique_together={('user', 'app', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='grouppermission',
            unique_together={('group', 'contenttype')},
        ),
        migrations.AlterUniqueTogether(
            name='groupfield',
            unique_together={('group', 'field')},
        ),
        migrations.AlterUniqueTogether(
            name='groupcontenttype',
            unique_together={('group', 'app', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('field', 'value')},
        ),
    ]
