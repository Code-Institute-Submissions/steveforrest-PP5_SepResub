# Generated by Django 3.2 on 2022-09-06 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='guest',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]