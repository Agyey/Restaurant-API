# Generated by Django 3.1.6 on 2021-02-17 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dish", options={"verbose_name_plural": "Dishes"},
        ),
        migrations.AlterField(
            model_name="restaurant",
            name="established",
            field=models.DateField(auto_now=True),
        ),
    ]
