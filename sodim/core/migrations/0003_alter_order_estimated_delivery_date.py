# Generated by Django 5.2 on 2025-05-20 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateField(null=True),
        ),
    ]
