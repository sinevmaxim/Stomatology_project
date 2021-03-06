# Generated by Django 3.1.4 on 2020-12-12 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_auto_20201212_0251'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('comment', models.TextField(blank=True, max_length=500)),
                ('is_closed', models.BooleanField(default=False)),
                ('is_visited', models.BooleanField(default=False)),
                ('doctor_comment', models.TextField(blank=True, max_length=500)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
