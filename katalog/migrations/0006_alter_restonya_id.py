# Generated by Django 5.1.2 on 2024-10-25 18:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0005_alter_restonya_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restonya',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]