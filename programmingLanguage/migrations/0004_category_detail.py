# Generated by Django 3.1.7 on 2021-04-01 08:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programmingLanguage', '0003_auto_20210401_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]