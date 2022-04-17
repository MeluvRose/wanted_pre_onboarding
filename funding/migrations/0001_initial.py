# Generated by Django 4.0.4 on 2022-04-16 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=30)),
                ('detail', models.TextField()),
                ('goal', models.IntegerField()),
                ('date_limit', models.DateField(auto_now_add=True)),
                ('price_per_time', models.IntegerField()),
            ],
        ),
    ]
