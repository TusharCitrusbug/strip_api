# Generated by Django 3.1.4 on 2022-04-28 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20220428_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='plan_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
