# Generated by Django 3.2.8 on 2021-11-25 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_rename_category_category_category_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
