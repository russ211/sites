# Generated by Django 2.0 on 2019-12-06 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20191206_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]