# Generated by Django 3.0.5 on 2020-06-11 08:38

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0018_auto_20200611_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='desc',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]
