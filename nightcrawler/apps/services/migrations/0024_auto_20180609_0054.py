# Generated by Django 2.0.5 on 2018-06-09 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0023_auto_20180609_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collecteddata',
            old_name='num_news',
            new_name='to_num',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='total_num',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
