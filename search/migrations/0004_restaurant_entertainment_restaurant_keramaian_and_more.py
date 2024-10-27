# Generated by Django 5.1.2 on 2024-10-26 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_alter_restaurant_jarak'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='entertainment',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='keramaian',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='suasana',
            field=models.CharField(default=0, max_length=266),
            preserve_default=False,
        ),
    ]
