# Generated by Django 4.1.2 on 2022-10-10 12:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_delete_bids_delete_comments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
