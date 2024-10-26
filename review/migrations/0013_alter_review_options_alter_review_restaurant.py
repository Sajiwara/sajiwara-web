# Generated by Django 5.1.2 on 2024-10-25 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katalog', '0011_delete_resto_id_alter_restonya_id'),
        ('review', '0012_alter_review_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={},
        ),
        migrations.AlterField(
            model_name='review',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='katalog.restonya'),
        ),
    ]
