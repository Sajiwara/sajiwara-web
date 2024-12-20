# Generated by Django 5.1.2 on 2024-10-22 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resto', models.CharField(max_length=100)),
                ('menu', models.CharField(max_length=300)),
                ('wanted_menu', models.BooleanField(default=False)),
                ('tried', models.BooleanField(default=False)),
            ],
        ),
    ]
