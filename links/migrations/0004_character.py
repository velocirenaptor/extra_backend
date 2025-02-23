# Generated by Django 4.2.13 on 2025-01-09 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('source', models.TextField(blank=True)),
                ('picture', models.URLField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
