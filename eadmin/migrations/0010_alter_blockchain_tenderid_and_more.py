# Generated by Django 5.0.1 on 2024-02-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eadmin", "0009_blockchain_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blockchain",
            name="tenderid",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="tendercotated",
            name="tenderid",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="tendercotated",
            name="userid",
            field=models.CharField(max_length=100),
        ),
    ]