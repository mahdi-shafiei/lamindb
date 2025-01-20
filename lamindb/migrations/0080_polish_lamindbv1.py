# Generated by Django 5.2 on 2025-01-20 04:42

import django.db.models.deletion
import django.db.models.functions.datetime
from django.db import migrations, models

import lamindb.base.fields
import lamindb.base.ids
import lamindb.base.users
import lamindb.models


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0079_alter_rundata_value_json_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="persons",
        ),
        migrations.AddField(
            model_name="project",
            name="is_type",
            field=lamindb.base.fields.BooleanField(
                blank=True, db_index=True, default=None, null=True
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="predecessors",
            field=models.ManyToManyField(
                related_name="successors", to="lamindb.project"
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=None,
                editable=False,
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_20,
                editable=False,
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_12,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_8,
                editable=False,
                max_length=8,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="type",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="records",
                to="lamindb.project",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_12,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="reference",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_12,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_20,
                editable=False,
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="schema",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=None,
                editable=False,
                max_length=20,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="space",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_default="00000000",
                db_index=True,
                default="00000000",
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="storage",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_12,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="tidytable",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_12,
                editable=False,
                max_length=12,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="transform",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=None,
                editable=False,
                max_length=16,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="ulabel",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=lamindb.base.ids.base62_8,
                editable=False,
                max_length=8,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="uid",
            field=lamindb.base.fields.CharField(
                blank=True,
                db_index=True,
                default=None,
                editable=False,
                max_length=8,
                unique=True,
            ),
        ),
        migrations.CreateModel(
            name="PersonProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(
                        blank=True,
                        db_default=django.db.models.functions.datetime.Now(),
                        db_index=True,
                        editable=False,
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "role",
                    lamindb.base.fields.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
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
                    "person",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.person",
                    ),
                ),
                (
                    "project",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_person",
                        to="lamindb.project",
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
            ],
            options={
                "unique_together": {("person", "project")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="project",
            name="people",
            field=models.ManyToManyField(
                related_name="projects",
                through="lamindb.PersonProject",
                to="lamindb.person",
            ),
        ),
        migrations.AlterField(
            model_name="rundata",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="_rundata",
                to="lamindb.run",
            ),
        ),
        migrations.AddField(
            model_name="schema",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="paramvalue",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="reference",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="started_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="runparamvalue",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="schema",
            name="name",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=150, null=True
            ),
        ),
        migrations.AlterField(
            model_name="space",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="tidytable",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="transform",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="transform",
            name="updated_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="ulabel",
            name="description",
            field=lamindb.base.fields.CharField(
                blank=True, db_index=True, default=None, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=lamindb.base.fields.DateTimeField(
                blank=True,
                db_default=django.db.models.functions.datetime.Now(),
                db_index=True,
                editable=False,
            ),
        ),
        migrations.CreateModel(
            name="RunULabel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
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
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_ulabel",
                        to="lamindb.run",
                    ),
                ),
                (
                    "ulabel",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_run",
                        to="lamindb.ulabel",
                    ),
                ),
            ],
            options={
                "unique_together": {("run", "ulabel")},
            },
            bases=(models.Model, lamindb.models.LinkORM),
        ),
        migrations.AddField(
            model_name="run",
            name="ulabels",
            field=models.ManyToManyField(
                related_name="runs", through="lamindb.RunULabel", to="lamindb.ulabel"
            ),
        ),
        migrations.RenameModel(
            old_name="TidyTable",
            new_name="FlexTable",
        ),
        migrations.RenameModel(
            old_name="TidyTableData",
            new_name="FlexTableData",
        ),
        migrations.RenameIndex(
            model_name="flextable",
            new_name="lamindb_fle_uid_e6f216_idx",
            old_name="lamindb_tid_uid_3a6e54_idx",
        ),
        migrations.RenameIndex(
            model_name="flextable",
            new_name="lamindb_fle_name_568594_idx",
            old_name="lamindb_tid_name_50c5de_idx",
        ),
        migrations.RenameIndex(
            model_name="flextabledata",
            new_name="lamindb_fle_tidytab_1674c1_idx",
            old_name="lamindb_tid_tidytab_b35a4d_idx",
        ),
        migrations.RenameIndex(
            model_name="flextabledata",
            new_name="lamindb_fle_feature_830e49_idx",
            old_name="lamindb_tid_feature_5a0b1f_idx",
        ),
        migrations.RenameIndex(
            model_name="flextabledata",
            new_name="lamindb_fle_param_i_4149cb_idx",
            old_name="lamindb_tid_param_i_16c884_idx",
        ),
        migrations.RemoveField(
            model_name="flextabledata",
            name="value_upath",
        ),
        migrations.RemoveField(
            model_name="rundata",
            name="value_upath",
        ),
    ]
