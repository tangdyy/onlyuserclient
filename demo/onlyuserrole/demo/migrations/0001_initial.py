# Generated by Django 2.2.4 on 2020-03-25 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoleDemo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号码')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
                ('idcord', models.EmailField(max_length=18, verbose_name='身份证号码')),
                ('owner', models.CharField(max_length=24, verbose_name='拥有我')),
            ],
        ),
    ]