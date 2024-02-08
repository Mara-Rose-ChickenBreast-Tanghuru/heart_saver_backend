# Generated by Django 5.0.1 on 2024-02-07 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('medicalCondition', models.CharField(max_length=500, null=True)),
                ('etc', models.CharField(max_length=500, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HeartRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hrv', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heart_rates', to='member.member')),
            ],
        ),
    ]
