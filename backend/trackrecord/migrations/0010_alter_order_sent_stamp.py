# Generated by Django 4.1.3 on 2023-03-12 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackrecord', '0009_alter_position_entry_stamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sent_stamp',
            field=models.DateTimeField(),
        ),
    ]
