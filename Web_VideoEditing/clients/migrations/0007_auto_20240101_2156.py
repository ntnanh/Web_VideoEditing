# Generated by Django 2.2.6 on 2024-01-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_upload_path_image_upload_title_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtitle',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userupload',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
