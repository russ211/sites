# Generated by Django 2.0 on 2019-12-06 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userinfo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(blank=True, max_length=255, upload_to=''),
        ),
    ]
