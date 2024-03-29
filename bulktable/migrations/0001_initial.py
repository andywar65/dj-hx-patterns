# Generated by Django 4.1.7 on 2023-03-15 17:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Row",
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
                ("title", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("#000000", "White"),
                            ("#FF0000", "Red"),
                            ("#00FF00", "Green"),
                            ("#0000FF", "Blue"),
                            ("#00FFFF", "Yellow"),
                        ],
                        default="#000000",
                        max_length=7,
                    ),
                ),
            ],
            options={
                "verbose_name": "Row",
                "verbose_name_plural": "Rows",
            },
        ),
    ]
