# Generated by Django 5.0 on 2024-02-16 11:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_rename_reviews_review"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="order",
        ),
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
