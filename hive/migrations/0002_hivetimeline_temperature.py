# Generated by Django 2.1.7 on 2019-04-22 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hive', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hivetimeline',
            name='temperature',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
