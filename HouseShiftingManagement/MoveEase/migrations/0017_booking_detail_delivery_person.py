# Generated by Django 4.2.4 on 2023-10-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEase', '0016_alter_booking_detail_service_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_detail',
            name='delivery_person',
            field=models.CharField(default=None, max_length=100),
        ),
    ]