# Generated by Django 2.1.4 on 2018-12-14 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181214_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_nums',
            field=models.IntegerField(default=0, verbose_name='阅读量'),
        ),
    ]
