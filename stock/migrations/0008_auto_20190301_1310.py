# Generated by Django 2.1.7 on 2019-03-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_item_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='total',
            field=models.IntegerField(max_length=255),
        ),
        migrations.AlterField(
            model_name='item',
            name='unit_cost',
            field=models.IntegerField(max_length=255),
        ),
    ]
