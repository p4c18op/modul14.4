# Generated by Django 4.2.10 on 2024-02-15 11:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='New', to='news.news')),
            ],
        ),
    ]
