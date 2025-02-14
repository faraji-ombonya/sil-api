# Generated by Django 5.1.5 on 2025-02-03 06:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthState',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=255)),
                ('nonce', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='GoogleCredential',
        ),
    ]
