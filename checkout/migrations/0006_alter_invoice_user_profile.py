# Generated by Django 3.2 on 2022-07-27 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('checkout', '0005_invoice_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice', to='profiles.userprofile'),
        ),
    ]