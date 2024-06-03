# Generated by Django 3.2.6 on 2024-05-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salary', '0004_alter_salary_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='total_salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
