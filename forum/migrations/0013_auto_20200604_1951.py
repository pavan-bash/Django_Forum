# Generated by Django 3.0.5 on 2020-06-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_auto_20200604_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporta',
            name='desc',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='reportq',
            name='desc',
            field=models.TextField(blank=True),
        ),
    ]
