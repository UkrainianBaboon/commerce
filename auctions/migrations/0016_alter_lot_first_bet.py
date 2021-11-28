# Generated by Django 3.2.8 on 2021-11-26 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_lot_first_bet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='first_bet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.bet'),
        ),
    ]
