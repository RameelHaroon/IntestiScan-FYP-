# Generated by Django 5.0.6 on 2024-05-24 08:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("name", models.CharField(max_length=100)),
                (
                    "email",
                    models.EmailField(
                        max_length=100,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=16,
                        validators=[django.core.validators.MinLengthValidator(8)],
                    ),
                ),
            ],
        ),
    ]