# Generated by Django 5.1.2 on 2024-10-23 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipemakanan', '0002_makanan_restoran'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makanan',
            name='restoran',
            field=models.CharField(default='Unknown Restaurant', max_length=255),
        ),
    ]
