# Generated by Django 3.1.4 on 2021-01-13 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210113_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='cardDetails',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.paymentmethod'),
        ),
    ]