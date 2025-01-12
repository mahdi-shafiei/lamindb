# Generated by Django 5.1 on 2024-06-19 09:56

import django.db.models.deletion
from django.db import migrations, models

import lamindb.models


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0054_alter_feature_previous_runs_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artifact",
            name="type",
            field=models.CharField(
                choices=[("dataset", "dataset"), ("model", "model"), ("code", "code")],
                db_index=True,
                default=None,
                max_length=20,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="ArtifactParamValue",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "artifact",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "paramvalue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.paramvalue",
                    ),
                ),
            ],
            options={
                "unique_together": {("artifact", "paramvalue")},
            },
            bases=(models.Model, lamindb.models.LinkORM),
        ),
        migrations.AddField(
            model_name="artifact",
            name="param_values",
            field=models.ManyToManyField(
                related_name="artifacts",
                through="lamindb.ArtifactParamValue",
                to="lamindb.paramvalue",
            ),
        ),
    ]