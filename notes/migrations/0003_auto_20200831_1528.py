# Generated by Django 3.0.8 on 2020-08-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]