# Generated by Django 3.1.6 on 2021-02-07 00:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=2)),
                ('set', models.CharField(max_length=3)),
                ('type', models.CharField(max_length=100)),
                ('rarity', models.CharField(max_length=40)),
                ('multiverse_id', models.CharField(max_length=10)),
                ('scryfall_id', models.CharField(max_length=48)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
