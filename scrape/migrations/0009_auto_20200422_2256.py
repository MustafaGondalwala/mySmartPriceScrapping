# Generated by Django 3.0.4 on 2020-04-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0008_auto_20200422_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
