# Generated by Django 4.2.8 on 2023-12-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_subtitle_table_alter_upload_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='path_image',
            field=models.FileField(max_length=200, upload_to='Files/'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='path_video',
            field=models.FileField(max_length=200, upload_to='Files/'),
        ),
    ]