# Generated by Django 3.2.6 on 2024-04-22 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JWTToken', '0002_jwttoken_is_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jwttoken',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
