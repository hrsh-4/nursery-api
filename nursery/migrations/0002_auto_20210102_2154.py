# Generated by Django 2.2 on 2021-01-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='image',
            field=models.ImageField(blank=True, default='../media/images/no_image.jpg', null=True, upload_to='../media/images/'),
        ),
    ]
