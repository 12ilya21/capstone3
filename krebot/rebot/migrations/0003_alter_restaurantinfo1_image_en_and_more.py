# Generated by Django 4.2.13 on 2024-06-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rebot', '0002_alter_restaurantinfo1_image_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantinfo1',
            name='image_en',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurantinfo1',
            name='image_ja',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurantinfo1',
            name='image_ko',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurantinfo1',
            name='image_zn',
            field=models.ImageField(upload_to=''),
        ),
    ]
