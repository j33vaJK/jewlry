# Generated by Django 5.0.6 on 2024-08-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_diamondproduct_fixed_mrp_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goldproduct',
            name='size',
            field=models.CharField(default='Type the ornament size', max_length=50, verbose_name='Size'),
        ),
    ]
