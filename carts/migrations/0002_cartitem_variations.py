# Generated by Django 3.2.8 on 2021-10-30 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_variation'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='Store.Variation'),
        ),
    ]
