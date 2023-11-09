# Generated by Django 4.2.4 on 2023-10-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoveEase', '0019_customer_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='customers_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('rating', models.IntegerField()),
                ('comments', models.TextField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='customer_review',
        ),
    ]