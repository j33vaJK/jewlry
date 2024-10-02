# Generated by Django 5.0.6 on 2024-07-31 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_goldproduct_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='diamondproduct',
            name='size',
            field=models.CharField(default='Type the ornement size', max_length=50, verbose_name='Size'),
        ),
        migrations.AddField(
            model_name='silverproduct',
            name='size',
            field=models.CharField(default='Type the ornement size', max_length=50, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='goldproduct',
            name='size',
            field=models.CharField(default='Type the ornement size', max_length=50, verbose_name='Size'),
        ),
    ]
