# Generated by Django 5.2 on 2025-01-15 22:25

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import django.db.models.functions.datetime
from django.db import migrations, models

import lamindb.base.fields
import lamindb.base.ids
import lamindb.base.users
import lamindb.models


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0077_lamindbv1_part6b"),
    ]

    operations = [
        migrations.CreateModel(
            name="TidyTable",
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
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(
                        blank=True,
                        db_default=django.db.models.functions.datetime.Now(),
                        db_index=True,
                        editable=False,
                    ),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(
                        blank=True,
                        db_default=django.db.models.functions.datetime.Now(),
                        db_index=True,
                        editable=False,
                    ),
                ),
                (
                    "_branch_code",
                    models.SmallIntegerField(db_default=1, db_index=True, default=1),
                ),
                (
                    "_aux",
                    lamindb.base.fields.JSONField(
                        blank=True, db_default=None, default=None, null=True
                    ),
                ),
                (
                    "uid",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=lamindb.base.ids.base62_12,
                        max_length=12,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lamindb.base.fields.CharField(
                        blank=True, default=None, max_length=255
                    ),
                ),
                (
                    "is_type",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "description",
                    lamindb.base.fields.TextField(blank=True, default=None),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "projects",
                    models.ManyToManyField(
                        related_name="_tidytables", to="lamindb.project"
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
                (
                    "schema",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="lamindb.schema",
                    ),
                ),
                (
                    "space",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        db_default=1,
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lamindb.space",
                    ),
                ),
                (
                    "type",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="records",
                        to="lamindb.tidytable",
                    ),
                ),
                (
                    "ulabels",
                    models.ManyToManyField(
                        related_name="_tidytables", to="lamindb.ulabel"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TidyTableData",
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
                (
                    "row",
                    lamindb.base.fields.IntegerField(
                        blank=True, help_text="Use -1 for result data"
                    ),
                ),
                ("value_int", models.BigIntegerField(blank=True, null=True)),
                ("value_float", models.FloatField(blank=True, null=True)),
                ("value_str", models.TextField(blank=True, null=True)),
                (
                    "value_upath",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("value_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "value_json",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                (
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.feature",
                    ),
                ),
                (
                    "param",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.param",
                    ),
                ),
                (
                    "space",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        db_default=1,
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lamindb.space",
                    ),
                ),
                (
                    "tidytable",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data",
                        to="lamindb.tidytable",
                    ),
                ),
                (
                    "value_artifact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "value_collection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.collection",
                    ),
                ),
                (
                    "value_person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.person",
                    ),
                ),
                (
                    "value_project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.project",
                    ),
                ),
                (
                    "value_ulabel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.ulabel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RunData",
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
                (
                    "row",
                    lamindb.base.fields.IntegerField(
                        blank=True, help_text="Use -1 for result data"
                    ),
                ),
                ("value_int", models.BigIntegerField(blank=True, null=True)),
                ("value_float", models.FloatField(blank=True, null=True)),
                ("value_str", models.TextField(blank=True, null=True)),
                (
                    "value_upath",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("value_datetime", models.DateTimeField(blank=True, null=True)),
                (
                    "value_json",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                (
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.feature",
                    ),
                ),
                (
                    "param",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.param",
                    ),
                ),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data",
                        to="lamindb.run",
                    ),
                ),
                (
                    "space",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        db_default=1,
                        default=1,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lamindb.space",
                    ),
                ),
                (
                    "value_artifact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "value_collection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.collection",
                    ),
                ),
                (
                    "value_person",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.person",
                    ),
                ),
                (
                    "value_project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.project",
                    ),
                ),
                (
                    "value_ulabel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lamindb.ulabel",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["run", "row"], name="lamindb_run_run_id_c02e71_idx"
                    ),
                    models.Index(
                        fields=["feature"], name="lamindb_run_feature_a37229_idx"
                    ),
                    models.Index(
                        fields=["param"], name="lamindb_run_param_i_cee058_idx"
                    ),
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(
                                ("feature__isnull", False), ("param__isnull", True)
                            ),
                            models.Q(
                                ("feature__isnull", True), ("param__isnull", False)
                            ),
                            _connector="OR",
                        ),
                        name="run_data_feature_param_mutex",
                    ),
                    models.UniqueConstraint(
                        fields=("run", "row", "feature", "param"),
                        name="run_data_unique",
                    ),
                ],
            },
        ),
        migrations.AddIndex(
            model_name="tidytable",
            index=models.Index(fields=["uid"], name="lamindb_tid_uid_3a6e54_idx"),
        ),
        migrations.AddIndex(
            model_name="tidytable",
            index=models.Index(fields=["name"], name="lamindb_tid_name_50c5de_idx"),
        ),
        migrations.AddIndex(
            model_name="tidytabledata",
            index=models.Index(
                fields=["tidytable", "row"], name="lamindb_tid_tidytab_b35a4d_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tidytabledata",
            index=models.Index(
                fields=["feature"], name="lamindb_tid_feature_5a0b1f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tidytabledata",
            index=models.Index(fields=["param"], name="lamindb_tid_param_i_16c884_idx"),
        ),
        migrations.AddConstraint(
            model_name="tidytabledata",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    models.Q(("feature__isnull", False), ("param__isnull", True)),
                    models.Q(("feature__isnull", True), ("param__isnull", False)),
                    _connector="OR",
                ),
                name="tidy_table_data_feature_param_mutex",
            ),
        ),
        migrations.AddConstraint(
            model_name="tidytabledata",
            constraint=models.UniqueConstraint(
                fields=("tidytable", "row", "feature", "param"),
                name="tidy_table_data_unique",
            ),
        ),
    ]