# Generated by Django 5.1 on 2024-11-20 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingsystem', '0005_booking_vehicle_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='vehicle_type',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='type',
            field=models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Van', 'Van'), ('Truck', 'Truck'), ('Bus', 'Bus'), ('Motorcycle', 'Motorcycle'), ('Electric Car', 'Electric Car')], max_length=50),
        ),
    ]
