# Generated by Django 2.2 on 2024-05-27 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('detailing_type', models.CharField(max_length=20)),
                ('forecast_data', models.TextField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]