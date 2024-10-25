# Generated by Django 5.1.2 on 2024-10-22 05:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('jenis_makanan', models.CharField(max_length=266)),
                ('rating', models.FloatField()),
            ],
        ),
    ]
