# Generated by Django 5.1.2 on 2024-10-27 01:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_restaurant_entertainment_restaurant_keramaian_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_name', models.CharField(blank=True, max_length=255, null=True)),
                ('query_jenis', models.CharField(blank=True, max_length=255, null=True)),
                ('query_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('sort_by', models.CharField(default='nama', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_histories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]