# Generated by Django 5.1.5 on 2025-02-03 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sub',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
