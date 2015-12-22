# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('EmailAddress', models.EmailField(max_length=254, serialize=False, primary_key=True)),
                ('Key', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Order', models.IntegerField()),
                ('Place', models.CharField(max_length=30)),
                ('Comment', models.TextField()),
                ('EmailAddress', models.ForeignKey(to='travel.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Province', models.CharField(max_length=30)),
                ('City', models.CharField(max_length=30)),
                ('Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=30)),
                ('Gender', models.CharField(max_length=10)),
                ('Age', models.IntegerField()),
                ('Email', models.EmailField(max_length=254)),
                ('Silence', models.BooleanField()),
                ('Active', models.BooleanField()),
                ('Chat', models.BooleanField()),
                ('MissPast', models.BooleanField()),
                ('Discription', models.CharField(max_length=80)),
                ('EmailAddress', models.ForeignKey(to='travel.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Willgo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('From', models.CharField(max_length=20)),
                ('Province', models.CharField(max_length=20)),
                ('City', models.CharField(max_length=20)),
                ('Date', models.DateField()),
                ('Time', models.IntegerField()),
                ('Low', models.DecimalField(max_digits=6, decimal_places=0)),
                ('High', models.DecimalField(max_digits=6, decimal_places=0)),
                ('Status', models.CharField(max_length=20)),
                ('EmailAddress', models.ForeignKey(to='travel.User')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='Mem',
            field=models.ManyToManyField(to='travel.User'),
        ),
        migrations.AddField(
            model_name='team',
            name='Owner',
            field=models.ForeignKey(to='travel.Account'),
        ),
    ]
