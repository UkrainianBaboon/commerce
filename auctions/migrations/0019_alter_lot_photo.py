# Generated by Django 3.2.8 on 2021-11-29 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_lot_first_bet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='photo',
            field=models.URLField(blank=True),
        ),
    ]
