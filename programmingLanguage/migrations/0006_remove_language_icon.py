# Generated by Django 3.1.7 on 2021-04-01 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programmingLanguage', '0005_auto_20210401_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='icon',
        ),
    ]
