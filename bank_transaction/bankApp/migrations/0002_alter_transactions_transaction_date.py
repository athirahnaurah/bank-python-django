# Generated by Django 4.2.5 on 2023-09-18 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='transaction_date',
            field=models.DateTimeField(),
        ),
    ]
