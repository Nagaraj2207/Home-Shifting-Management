# Generated by Django 4.2.4 on 2023-09-20 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEase', '0003_user_registration_delete_registration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_registration',
            old_name='country',
            new_name='state',
        ),
    ]
