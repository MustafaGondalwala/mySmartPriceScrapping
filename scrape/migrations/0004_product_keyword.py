# Generated by Django 3.0.4 on 2020-04-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='keyword',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
