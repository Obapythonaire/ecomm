# Generated by Django 5.0 on 2023-12-22 19:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playground", "0004_address_zip"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(
                fields=["last_name", "first_name"],
                name="playground__last_na_400a69_idx",
            ),
        ),
    ]
