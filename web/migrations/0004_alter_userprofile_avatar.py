# Generated by Django 4.2 on 2023-04-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_video_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/nofoto.jpg', null=True, upload_to='avatars/', verbose_name='Аватарка'),
        ),
    ]
