# Generated by Django 5.0.1 on 2024-02-01 17:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eadmin", "0004_tender_tenderno"),
    ]

    operations = [
        migrations.AddField(
            model_name="tender",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
