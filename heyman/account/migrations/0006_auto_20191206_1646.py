# Generated by Django 2.0 on 2019-12-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20191206_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, upload_to='avatars/'),
        ),
    ]