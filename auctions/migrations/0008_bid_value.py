# Generated by Django 3.1.3 on 2021-02-20 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210111_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
