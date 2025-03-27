# Generated by Django 5.1.7 on 2025-03-26 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EMI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('principal_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_service.loan')),
            ],
        ),
    ]
