# Generated by Django 3.2.8 on 2021-12-17 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0038_auto_20211217_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='auctions.lot'),
        ),
    ]
