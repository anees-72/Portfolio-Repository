# Generated by Django 5.1.4 on 2025-01-17 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_listing_current_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
