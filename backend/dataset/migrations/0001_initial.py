# Generated by Django 4.0 on 2023-05-01 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NaicsCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'securities',
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SicCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TempSymbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=32, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('exchange', models.CharField(blank=True, max_length=16, null=True)),
                ('listed_market', models.CharField(blank=True, max_length=16, null=True)),
                ('security_type', models.CharField(blank=True, max_length=16, null=True)),
                ('sic', models.CharField(blank=True, max_length=8, null=True)),
                ('frontmonth', models.CharField(blank=True, max_length=1, null=True)),
                ('naics', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'ordering': ['symbol'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('frontmonth', models.CharField(blank=True, max_length=1, null=True)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to='dataset.exchange')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to='dataset.market')),
                ('naics', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to='dataset.naicscode')),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to='dataset.security')),
                ('sic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to='dataset.siccode')),
            ],
            options={
                'ordering': ['exchange__code', 'code'],
                'abstract': False,
            },
        ),
    ]
