# Generated by Django 5.1.2 on 2024-10-27 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_alter_searchhistory_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SearchHistory',
        ),
    ]
