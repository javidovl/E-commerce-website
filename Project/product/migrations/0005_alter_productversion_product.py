# Generated by Django 3.2.6 on 2021-11-14 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20211111_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productversion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_of_version', to='product.product'),
        ),
    ]
