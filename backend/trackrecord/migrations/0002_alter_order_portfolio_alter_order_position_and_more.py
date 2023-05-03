# Generated by Django 4.0 on 2023-05-02 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
        ('trackrecord', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trackrecord.portfolio'),
        ),
        migrations.AlterField(
            model_name='order',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trackrecord.position'),
        ),
        migrations.AlterField(
            model_name='order',
            name='symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.symbol'),
        ),
    ]
