# Generated by Django 5.0.4 on 2024-04-04 11:27

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        # ("auth", "0014_user_birth"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "clinic_address",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        default=0.0,
                        max_digits=2,
                        null=True,
                    ),
                ),
                (
                    "num_of_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=1,
                        default=0.0,
                        max_digits=5,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Doctor",
                "ordering": ["id"],
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Patient",
                "ordering": ["id"],
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
