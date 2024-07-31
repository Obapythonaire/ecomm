# Generated by Django 5.0 on 2023-12-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playground", "0003_added_slug_field_to_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="zip",
            field=models.CharField(default="-", max_length=6),
            preserve_default=False,
        ),
    ]