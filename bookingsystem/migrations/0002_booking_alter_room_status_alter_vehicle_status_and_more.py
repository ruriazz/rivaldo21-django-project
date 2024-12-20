# Generated by Django 5.1 on 2024-11-15 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookingsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('Room', 'Room'), ('Vehicle', 'Vehicle')], max_length=50)),
                ('resource_id', models.IntegerField()),
                ('requester_name', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('In Use', 'In Use'), ('Under Maintenance', 'Under Maintenance')], max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('In Use', 'In Use'), ('Under Maintenance', 'Under Maintenance')], max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='type',
            field=models.CharField(choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Van', 'Van'), ('Truck', 'Truck')], max_length=50),
        ),
    ]
