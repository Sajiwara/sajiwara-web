# Generated by Django 5.1.2 on 2024-10-25 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_alter_restor_id_alter_review_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-date_posted'], 'verbose_name_plural': 'Reviews'},
        ),
    ]