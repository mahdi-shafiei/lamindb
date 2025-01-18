# Generated by Django 5.2 on 2025-01-13 05:55

import django.core.validators
import django.db.models.deletion
import lamindb_setup
from django.db import migrations, models

import lamindb.base.fields
import lamindb.base.ids
import lamindb.base.users
import lamindb.models


def migrate_data(apps, schema_editor):
    """Check if source table exists and run migration if it does."""
    db = schema_editor.connection
    cursor = db.cursor()

    # Check if table exists - works in both SQLite and PostgreSQL
    if db.vendor == "sqlite":
        cursor.execute("""
            SELECT count(*)
            FROM sqlite_master
            WHERE type='table' AND name='ourprojects_reference';
        """)
    else:  # postgresql
        cursor.execute("""
            SELECT count(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'ourprojects_reference';
        """)

    table_exists = cursor.fetchone()[0] > 0
    if not table_exists:
        return

    # Get initial counts
    cursor.execute("SELECT COUNT(*) FROM ourprojects_reference")
    old_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lamindb_reference")
    initial_target_count = cursor.fetchone()[0]

    # Begin transaction
    cursor.execute("BEGIN")
    try:
        # Copy core tables, adding empty JSON for aux field
        cursor.execute("""
            INSERT INTO lamindb_reference(
                id, created_at, updated_at, created_by_id, uid, name, abbr, url,
                pubmed_id, doi, preprint, public, journal, description, text,
                published_at
            )
            SELECT
                id, created_at, updated_at, created_by_id, uid, name, abbr, url,
                pubmed_id, doi, preprint, public, journal, description, text,
                published_at
            FROM ourprojects_reference
        """)

        cursor.execute("""
            INSERT INTO lamindb_person(
                id, created_at, updated_at, created_by_id, uid, name, email,
                external
            )
            SELECT
                id, created_at, updated_at, created_by_id, uid, name, email,
                external
            FROM ourprojects_person
        """)

        cursor.execute("""
            INSERT INTO lamindb_project(
                id, created_at, updated_at, created_by_id, uid, name, abbr,
                url
            )
            SELECT
                id, created_at, updated_at, created_by_id, uid, name, abbr,
                url
            FROM ourprojects_project
        """)

        # Copy many-to-many relationships with aux field
        cursor.execute("""
            INSERT INTO lamindb_artifactreference(
                id, created_at, created_by_id, artifact_id, reference_id,
                feature_id, label_ref_is_name, feature_ref_is_name
            )
            SELECT
                id, created_at, created_by_id, artifact_id, reference_id,
                feature_id, label_ref_is_name, feature_ref_is_name
            FROM ourprojects_artifactreference
        """)

        cursor.execute("""
            INSERT INTO lamindb_transformreference(
                id, created_at, created_by_id, transform_id, reference_id
            )
            SELECT
                id, created_at, created_by_id, transform_id, reference_id
            FROM ourprojects_transformreference
        """)

        cursor.execute("""
            INSERT INTO lamindb_collectionreference(
                id, created_at, created_by_id, collection_id, reference_id
            )
            SELECT
                id, created_at, created_by_id, collection_id, reference_id
            FROM ourprojects_collectionreference
        """)

        cursor.execute("""
            INSERT INTO lamindb_artifactproject(
                id, created_at, created_by_id, artifact_id, project_id,
                feature_id, label_ref_is_name, feature_ref_is_name
            )
            SELECT
                id, created_at, created_by_id, artifact_id, project_id,
                feature_id, label_ref_is_name, feature_ref_is_name
            FROM ourprojects_artifactproject
        """)

        cursor.execute("""
            INSERT INTO lamindb_transformproject(
                id, created_at, created_by_id, transform_id, project_id
            )
            SELECT
                id, created_at, created_by_id, transform_id, project_id
            FROM ourprojects_transformproject
        """)

        cursor.execute("""
            INSERT INTO lamindb_collectionproject(
                id, created_at, created_by_id, collection_id, project_id
            )
            SELECT
                id, created_at, created_by_id, collection_id, project_id
            FROM ourprojects_collectionproject
        """)

        # Verify migration
        cursor.execute("SELECT COUNT(*) FROM lamindb_reference")
        final_count = cursor.fetchone()[0]
        expected_count = initial_target_count + old_count

        if final_count == expected_count:
            # Clean up ourprojects content
            cursor.execute("DELETE FROM django_migrations WHERE app = 'ourprojects'")

            # Drop tables - using standard SQL
            tables = [
                "ourprojects_reference",
                "ourprojects_person",
                "ourprojects_project",
                "ourprojects_artifactreference",
                "ourprojects_transformreference",
                "ourprojects_collectionreference",
                "ourprojects_artifactproject",
                "ourprojects_transformproject",
                "ourprojects_collectionproject",
            ]

            for table in tables:
                if db.vendor == "sqlite":
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                else:  # postgresql
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")

            cursor.execute("COMMIT")
            print(
                "Data migration from ourprojects to lamindb successful, you can now access ourprojects data through lamindb"
            )
        else:
            cursor.execute("ROLLBACK")
            raise Exception("Migration failed: Record count mismatch")

    except Exception as e:
        cursor.execute("ROLLBACK")
        raise e


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0072_remove_user__branch_code_remove_user_aux_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtifactProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "label_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "feature_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "artifact",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.artifact",
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
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactproject",
                        to="lamindb.feature",
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
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="ArtifactReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "label_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "feature_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "artifact",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.artifact",
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
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactreference",
                        to="lamindb.feature",
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
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="CollectionProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "collection",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.collection",
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
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="CollectionReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "collection",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.collection",
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
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                (
                    "_branch_code",
                    models.SmallIntegerField(db_default=1, db_index=True, default=1),
                ),
                ("aux", models.JSONField(db_default=None, default=None, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=lamindb.base.ids.base62_8,
                        max_length=8,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lamindb.base.fields.CharField(
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "email",
                    lamindb.base.fields.EmailField(
                        blank=True, default=None, max_length=254, null=True
                    ),
                ),
                (
                    "external",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=True
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
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
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
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                (
                    "_branch_code",
                    models.SmallIntegerField(db_default=1, db_index=True, default=1),
                ),
                ("aux", models.JSONField(db_default=None, default=None, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
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
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "abbr",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "url",
                    lamindb.base.fields.URLField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="projects",
                        through="lamindb.ArtifactProject",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "collections",
                    models.ManyToManyField(
                        related_name="projects",
                        through="lamindb.CollectionProject",
                        to="lamindb.collection",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        related_name="projects", to="lamindb.person"
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
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
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
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.AddField(
            model_name="collectionproject",
            name="project",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_collection",
                to="lamindb.project",
            ),
        ),
        migrations.AddField(
            model_name="artifactproject",
            name="project",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="lamindb.project",
            ),
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                (
                    "_branch_code",
                    models.SmallIntegerField(db_default=1, db_index=True, default=1),
                ),
                ("aux", models.JSONField(db_default=None, default=None, null=True)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
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
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "abbr",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("url", lamindb.base.fields.URLField(blank=True, null=True)),
                (
                    "pubmed_id",
                    lamindb.base.fields.BigIntegerField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "doi",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=255,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Must be a DOI (e.g., 10.1000/xyz123 or https://doi.org/10.1000/xyz123)",
                                regex="^(?:https?://(?:dx\\.)?doi\\.org/|doi:|DOI:)?10\\.\\d+/.*$",
                            )
                        ],
                    ),
                ),
                (
                    "preprint",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=False
                    ),
                ),
                (
                    "public",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=True
                    ),
                ),
                (
                    "journal",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "description",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "text",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "published_at",
                    lamindb.base.fields.DateField(blank=True, default=None, null=True),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="references",
                        through="lamindb.ArtifactReference",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "authors",
                    models.ManyToManyField(
                        related_name="references", to="lamindb.person"
                    ),
                ),
                (
                    "collections",
                    models.ManyToManyField(
                        related_name="references",
                        through="lamindb.CollectionReference",
                        to="lamindb.collection",
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
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
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
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="references",
            field=models.ManyToManyField(
                related_name="projects", to="lamindb.reference"
            ),
        ),
        migrations.AddField(
            model_name="collectionreference",
            name="reference",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_collection",
                to="lamindb.reference",
            ),
        ),
        migrations.AddField(
            model_name="artifactreference",
            name="reference",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="lamindb.reference",
            ),
        ),
        migrations.CreateModel(
            name="TransformProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
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
                    "project",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_transform",
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
                (
                    "transform",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.transform",
                    ),
                ),
            ],
            options={
                "unique_together": {("transform", "project")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="project",
            name="transforms",
            field=models.ManyToManyField(
                related_name="projects",
                through="lamindb.TransformProject",
                to="lamindb.transform",
            ),
        ),
        migrations.CreateModel(
            name="TransformReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
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
                    "reference",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_transform",
                        to="lamindb.reference",
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
                    "transform",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.transform",
                    ),
                ),
            ],
            options={
                "unique_together": {("transform", "reference")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="reference",
            name="transforms",
            field=models.ManyToManyField(
                related_name="references",
                through="lamindb.TransformReference",
                to="lamindb.transform",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="collectionproject",
            unique_together={("collection", "project")},
        ),
        migrations.AlterUniqueTogether(
            name="artifactproject",
            unique_together={("artifact", "project", "feature")},
        ),
        migrations.AlterUniqueTogether(
            name="collectionreference",
            unique_together={("collection", "reference")},
        ),
        migrations.AlterUniqueTogether(
            name="artifactreference",
            unique_together={("artifact", "reference", "feature")},
        ),
        migrations.RunPython(
            migrate_data,
        ),
    ]


if "ourprojects" in lamindb_setup.settings.instance.modules:
    Migration.dependencies += [
        ("ourprojects", "0003_alter_person_space_alter_project_space_and_more"),
    ]
