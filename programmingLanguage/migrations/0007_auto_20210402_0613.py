# Generated by Django 3.1.7 on 2021-04-02 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programmingLanguage', '0006_remove_language_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['name']},
        ),
    ]
