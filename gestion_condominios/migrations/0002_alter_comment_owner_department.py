# Generated by Django 3.2.4 on 2021-07-05 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_condominios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='owner_department',
            field=models.CharField(max_length=100),
        ),
    ]