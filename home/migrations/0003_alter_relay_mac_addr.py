# Generated by Django 5.0.3 on 2024-03-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_relay_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relay',
            name='mac_addr',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
