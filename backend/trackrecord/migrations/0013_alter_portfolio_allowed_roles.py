# Generated by Django 4.0 on 2023-04-26 17:21

import core.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackrecord', '0012_alter_permission_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='allowed_roles',
            field=core.forms.ChoiceArrayField(base_field=models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('subscriber', 'Subscriber'), ('guest', 'Guest')], default='owner', max_length=10), size=None),
        ),
    ]
