# Generated by Django 4.1.7 on 2023-03-22 20:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timeline", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phase",
            name="delay",
            field=models.IntegerField(default=0, help_text="In weeks"),
        ),
        migrations.AlterField(
            model_name="phase",
            name="duration",
            field=models.PositiveIntegerField(default=1, help_text="In weeks"),
        ),
        migrations.AlterField(
            model_name="phase",
            name="phase_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("LP0", "Other"),
                    ("LP1", "Feasibility study"),
                    ("LP2", "Preliminary design"),
                    ("LP3", "Definitive design"),
                    ("LP4", "Authoring"),
                    ("LP5", "Construction design"),
                    ("LP6", "Tender design"),
                    ("LP7", "Project management"),
                    ("LP8", "Construction supervision"),
                    ("LP9", "Maintenance design"),
                ],
                max_length=7,
                null=True,
            ),
        ),
    ]