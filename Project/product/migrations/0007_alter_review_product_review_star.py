# Generated by Django 3.2.6 on 2021-11-18 14:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_productversion_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review_product',
            name='review_star',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MinLengthValidator(5)]),
        ),
    ]
