# Generated by Django 3.2.8 on 2021-11-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20211126_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='first_bet',
            field=models.FloatField(),
        ),
    ]
