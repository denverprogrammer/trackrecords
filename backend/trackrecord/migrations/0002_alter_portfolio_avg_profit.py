# Generated by Django 4.1.3 on 2023-03-12 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackrecord', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='avg_profit',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]
