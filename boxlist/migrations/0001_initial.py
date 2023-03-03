# Generated by Django 4.1.7 on 2023-03-03 18:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("position", models.PositiveIntegerField(default=1)),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
                "ordering": ["position"],
            },
        ),
    ]
