# Generated by Django 5.1.1 on 2024-10-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_alter_review_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
