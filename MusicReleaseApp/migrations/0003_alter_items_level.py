# Generated by Django 4.1 on 2023-02-28 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicReleaseApp', '0002_remove_items_tab_image_items_artwork_items_music_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]