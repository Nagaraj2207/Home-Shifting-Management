# Generated by Django 4.2.4 on 2023-09-21 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEase', '0006_alter_user_registration_delivery_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_registration',
            name='contact',
            field=models.BigIntegerField(),
        ),
    ]
