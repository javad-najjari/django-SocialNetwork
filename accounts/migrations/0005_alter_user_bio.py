# Generated by Django 4.0.3 on 2022-03-31 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_bio_user_name_user_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default='Not imported', null=True),
        ),
    ]
