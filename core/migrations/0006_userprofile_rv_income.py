# Generated by Django 2.2.10 on 2020-09-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200903_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='rv_income',
            field=models.FloatField(default='0', max_length=5),
        ),
    ]
