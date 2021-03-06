# Generated by Django 3.1.6 on 2021-02-17 23:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20210218_0357"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="cuisines",
            field=models.ManyToManyField(blank=True, to="core.Cuisine"),
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="established",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
