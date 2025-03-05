# Generated by Django 5.2 on 2025-03-05 10:20

import django.db.models.deletion
import django.db.models.functions.datetime
from django.db import migrations, models

import lamindb.base.fields
import lamindb.base.users
import lamindb.models.record


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0089_subsequent_runs"),
    ]

    operations = [
        migrations.CreateModel(
            name="RunProject",
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
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "project",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_run",
                        to="lamindb.project",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.run",
                    ),
                ),
            ],
            options={
                "unique_together": {("run", "project")},
            },
            bases=(models.Model, lamindb.models.record.LinkORM),
        ),
        migrations.AddField(
            model_name="project",
            name="runs",
            field=models.ManyToManyField(
                related_name="projects", through="lamindb.RunProject", to="lamindb.run"
            ),
        ),
    ]
