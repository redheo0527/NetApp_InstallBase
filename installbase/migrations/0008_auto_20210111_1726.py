# Generated by Django 3.1.4 on 2021-01-11 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installbase', '0007_auto_20210111_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='licensed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='installbase',
            name='licensed',
        ),
        migrations.AddField(
            model_name='installbase',
            name='licensed',
            field=models.ManyToManyField(to='installbase.licensed'),
        ),
    ]