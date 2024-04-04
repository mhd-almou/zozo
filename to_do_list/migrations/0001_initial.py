# Generated by Django 5.0.4 on 2024-04-04 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="To_Do",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("aim", models.CharField(max_length=100)),
                ("goal", models.CharField(max_length=100)),
                ("is_done", models.BooleanField(default=False)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="doctor_appointments",
                        to="users.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_appointments",
                        to="users.patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "To_Do_list",
                "ordering": ["patient_id"],
            },
        ),
    ]
