# Generated by Django 5.1.2 on 2024-10-27 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0009_rename_search_query_searchhistory_nama_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchhistory',
            name='rating',
        ),
    ]
