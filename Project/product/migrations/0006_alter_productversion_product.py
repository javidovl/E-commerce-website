# Generated by Django 3.2.6 on 2021-11-16 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_productversion_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productversion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='product.product'),
        ),
    ]
