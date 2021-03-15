# Generated by Django 3.1.5 on 2021-02-28 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ics_part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.TextField()),
                ('part_description', models.TextField()),
                ('ea', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ics_inout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.TextField(null=True)),
                ('project_name', models.TextField(null=True)),
                ('inout', models.BooleanField(null=True)),
                ('ea', models.IntegerField(null=True)),
                ('ics_update', models.DateField(null=True)),
                ('user', models.TextField(null=True)),
                ('inout_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ics.ics_part')),
            ],
            options={
                'ordering': ['-part_num'],
            },
        ),
    ]
