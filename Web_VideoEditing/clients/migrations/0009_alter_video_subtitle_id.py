# Generated by Django 5.0 on 2024-01-02 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_alter_subtitle_id_alter_upload_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subtitle_id',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='clients.subtitle'),
        ),
    ]