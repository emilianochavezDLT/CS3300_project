# Generated by Django 4.2.6 on 2023-11-23 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundry_day', '0006_alter_laundryrequests_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='family_code',
            field=models.CharField(default=None, max_length=4, null=True),
        ),
    ]
