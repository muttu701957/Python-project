# Generated by Django 5.1.6 on 2025-03-28 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0010_notification_response_notification_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transplant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transplant_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='newapp.donordetails')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='newapp.hospitaldetail')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.recipient')),
            ],
        ),
    ]
