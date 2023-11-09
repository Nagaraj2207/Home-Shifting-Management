# Generated by Django 4.2.4 on 2023-09-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('MoveEasePerson', models.BooleanField(default=False)),
                ('delivery_person', models.BooleanField(default=False)),
                ('contact', models.BigIntegerField(unique=True)),
            ],
        ),
    ]
