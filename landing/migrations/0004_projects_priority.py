# Generated by Django 4.0.6 on 2022-08-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_remove_projectstranslation_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
