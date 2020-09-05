# Generated by Django 2.2.10 on 2020-09-05 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200903_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diamondgame',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'green'), ('red', 'red'), ('purple', 'purple'), ('red purple', 'red purple'), ('green purple', 'green purple')], default='unknown', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='goldgame',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'green'), ('red', 'red'), ('purple', 'purple'), ('red purple', 'red purple'), ('green purple', 'green purple')], default='unknown', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='othergame',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'green'), ('red', 'red'), ('purple', 'purple'), ('red purple', 'red purple'), ('green purple', 'green purple')], default='unknown', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='silvergame',
            name='color',
            field=models.CharField(blank=True, choices=[('green', 'green'), ('red', 'red'), ('purple', 'purple'), ('red purple', 'red purple'), ('green purple', 'green purple')], default='unknown', max_length=20, null=True),
        ),
    ]
