# Generated by Django 2.0.5 on 2018-06-08 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20180608_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsdata',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
