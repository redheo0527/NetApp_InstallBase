# Generated by Django 3.1.4 on 2021-01-07 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installbase', '0003_auto_20210106_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installbase',
            name='deleted',
            field=models.IntegerField(),
        ),
    ]