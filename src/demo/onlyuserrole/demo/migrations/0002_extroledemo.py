# Generated by Django 2.2.4 on 2020-05-23 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtRoleDemo',
            fields=[
                ('roledemo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='demo.RoleDemo')),
                ('name1', models.CharField(max_length=20, verbose_name='姓名')),
            ],
            bases=('demo.roledemo',),
        ),
    ]