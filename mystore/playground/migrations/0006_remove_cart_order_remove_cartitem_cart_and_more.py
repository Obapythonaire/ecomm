# Generated by Django 5.0 on 2023-12-25 22:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("playground", "0005_customer_playground__last_na_400a69_idx"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="order",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="cart",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="product",
        ),
        migrations.RemoveField(
            model_name="product",
            name="collection",
        ),
        migrations.RemoveField(
            model_name="order",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="order",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="product",
        ),
        migrations.RemoveField(
            model_name="product",
            name="promotion",
        ),
        migrations.DeleteModel(
            name="Address",
        ),
        migrations.DeleteModel(
            name="Cart",
        ),
        migrations.DeleteModel(
            name="CartItem",
        ),
        migrations.DeleteModel(
            name="Collection",
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
        migrations.DeleteModel(
            name="Order",
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
        migrations.DeleteModel(
            name="Product",
        ),
        migrations.DeleteModel(
            name="Promotion",
        ),
    ]