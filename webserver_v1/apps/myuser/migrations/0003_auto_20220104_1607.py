# Generated by Django 3.0.3 on 2022-01-04 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_auto_20211130_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='birth_day',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='email',
        ),
    ]
