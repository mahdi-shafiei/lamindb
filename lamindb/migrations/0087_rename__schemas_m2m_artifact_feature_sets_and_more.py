# Generated by Django 5.2 on 2025-02-13 12:00

import django.db.models.deletion
from django.db import migrations, models

import lamindb.base.fields


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0086_various"),
    ]

    operations = [
        migrations.RenameField(
            model_name="artifact",
            old_name="_schemas_m2m",
            new_name="feature_sets",
        ),
        migrations.AlterField(
            model_name="artifact",
            name="schema",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="validated_artifacts",
                to="lamindb.schema",
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="feature_sets",
            field=models.ManyToManyField(
                related_name="artifacts",
                through="lamindb.ArtifactSchema",
                to="lamindb.schema",
            ),
        ),
    ]
