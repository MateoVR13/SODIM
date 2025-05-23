# Generated by Django 5.2 on 2025-05-01 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('sent', 'Sent'), ('arrived', 'Arrived'), ('delivered', 'Delivered')], default='requested', max_length=10)),
                ('estimated_delivery_date', models.DateField()),
                ('actual_delivery_date', models.DateField(blank=True, null=True)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.patient')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.prescription')),
            ],
        ),
    ]
