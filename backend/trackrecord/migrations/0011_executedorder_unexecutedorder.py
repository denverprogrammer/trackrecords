# Generated by Django 4.1.3 on 2023-03-14 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackrecord', '0010_alter_order_sent_stamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutedOrder',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('trackrecord.order',),
        ),
        migrations.CreateModel(
            name='UnexecutedOrder',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('trackrecord.order',),
        ),
    ]
