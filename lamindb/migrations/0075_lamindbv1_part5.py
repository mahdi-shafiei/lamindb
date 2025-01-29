# Generated by Django 5.2 on 2025-01-13 14:10

import django.db.models.deletion
from django.db import migrations, models

import lamindb.base.fields
import lamindb.base.users
import lamindb.models


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0074_lamindbv1_part4"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FeatureSet",
            new_name="Schema",
        ),
        migrations.RenameModel(
            old_name="ArtifactFeatureSet",
            new_name="ArtifactSchema",
        ),
        migrations.RenameField(
            model_name="feature",
            old_name="feature_sets",
            new_name="schemas",
        ),
        migrations.RenameField(
            model_name="artifact",
            old_name="feature_sets",
            new_name="_schemas_m2m",
        ),
        migrations.RenameField(
            model_name="artifactschema",
            old_name="featureset",
            new_name="schema",
        ),
        migrations.RenameModel(
            old_name="FeatureSetFeature",
            new_name="SchemaFeature",
        ),
        migrations.RenameField(
            model_name="schemafeature",
            old_name="featureset",
            new_name="schema",
        ),
        migrations.AddField(
            model_name="artifact",
            name="schema",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="artifacts",
                to="lamindb.schema",
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="_schemas_m2m",
            field=models.ManyToManyField(
                related_name="_artifacts_m2m",
                through="lamindb.ArtifactSchema",
                to="lamindb.schema",
            ),
        ),
        migrations.AlterField(
            model_name="artifactschema",
            name="artifact",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="_links_schema",
                to="lamindb.artifact",
            ),
        ),
        migrations.AlterField(
            model_name="artifactschema",
            name="schema",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="_links_artifact",
                to="lamindb.schema",
            ),
        ),
        migrations.RemoveField(
            model_name="artifact",
            name="_curator",
        ),
        migrations.AddField(
            model_name="feature",
            name="_curation",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="array_size",
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="feature",
            name="proxy_dtype",
            field=lamindb.base.fields.CharField(
                blank=True, null=True, default=None, max_length=255
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="array_rank",
            field=models.SmallIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="feature",
            name="array_shape",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="_status_code",
            field=models.SmallIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name="project",
            name="end_date",
            field=lamindb.base.fields.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="start_date",
            field=lamindb.base.fields.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="schema",
            name="_curation",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="composite",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="components",
                to="lamindb.schema",
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="maximal_set",
            field=lamindb.base.fields.BooleanField(
                blank=True, db_index=True, default=False
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="minimal_set",
            field=lamindb.base.fields.BooleanField(
                blank=True, db_index=True, default=True
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="ordered_set",
            field=lamindb.base.fields.BooleanField(
                blank=True, db_index=True, default=False
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="otype",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=64, null=True
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="slot",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=100, null=True
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="validated_by",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="validated_schemas",
                to="lamindb.schema",
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="dtype",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="schema",
            name="hash",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=22, null=True
            ),
        ),
        migrations.CreateModel(
            name="SchemaParam",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "param",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.param",
                    ),
                ),
                (
                    "schema",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.schema",
                    ),
                ),
            ],
            options={
                "unique_together": {("schema", "param")},
            },
            bases=(models.Model, lamindb.models.LinkORM),
        ),
        migrations.AddField(
            model_name="param",
            name="schemas",
            field=models.ManyToManyField(
                related_name="params",
                through="lamindb.SchemaParam",
                to="lamindb.schema",
            ),
        ),
        migrations.RenameField(
            model_name="schema",
            old_name="registry",
            new_name="itype",
        ),
        migrations.AlterField(
            model_name="schema",
            name="itype",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=120, null=True
            ),
        ),
    ]


# if "bionty" in lamindb_setup.settings.instance.modules:
#     Migration.dependencies += [
#         ("bionty", "0046_alter_cellline__aux_alter_cellmarker__aux_and_more"),
#     ]
