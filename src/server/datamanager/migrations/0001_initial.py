"""
Copyright 2017-2024 SensiML Corporation

This file is part of SensiML™ Piccolo AI™.

SensiML Piccolo AI is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

SensiML Piccolo AI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with SensiML Piccolo AI. If not, see <https://www.gnu.org/licenses/>.
"""

# Generated by Django 3.2.12 on 2024-06-20 03:52

import datamanager.managers
import datamanager.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            """DO
        $do$
        BEGIN
        IF EXISTS (
            SELECT                       -- SELECT list can stay empty for this
            FROM   pg_user
            WHERE  usename = 'piccoloadmin' AND usesuper = 't') THEN
            CREATE EXTENSION IF NOT EXISTS tablefunc;
        END IF;
        END
        $do$;"""
        ),
        migrations.CreateModel(
            name="Capture",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("file", models.CharField(blank=True, max_length=255, null=True)),
                ("file_size", models.IntegerField(null=True)),
                ("number_samples", models.IntegerField(null=True)),
                ("max_sequence", models.IntegerField(null=True)),
                ("calculated_sample_rate", models.FloatField(null=True)),
                ("set_sample_rate", models.IntegerField(null=True)),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=36, unique=True),
                ),
                ("task", models.CharField(default=None, max_length=64, null=True)),
                (
                    "task_result",
                    models.CharField(default=None, max_length=128, null=True),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("last_modified_video", models.DateTimeField(default=None, null=True)),
                ("version", models.IntegerField(default=0)),
                ("format", models.CharField(default=".csv", max_length=10)),
                ("schema", models.JSONField(null=True)),
                (
                    "datatype",
                    models.SmallIntegerField(
                        choices=[(0, "Null"), (1, "Int32"), (2, "Float32")], default=0
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FeatureFile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=40, unique=True),
                ),
                ("name", models.CharField(max_length=200)),
                ("format", models.CharField(default="", max_length=200)),
                ("path", models.CharField(max_length=1024)),
                ("is_features", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("version", models.SmallIntegerField(default=2)),
                ("label_column", models.CharField(max_length=64, null=True)),
                ("number_rows", models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="KnowledgePack",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("execution_time", models.DateTimeField(auto_now=True)),
                ("neuron_array", models.JSONField(default=None, null=True)),
                ("model_results", models.JSONField(default=None, null=True)),
                ("configuration_index", models.CharField(max_length=40, null=True)),
                ("name", models.CharField(max_length=40, null=True)),
                ("model_index", models.CharField(max_length=40, null=True)),
                ("pipeline_summary", models.JSONField(default=None, null=True)),
                ("knowledgepack_summary", models.JSONField(default=None, null=True)),
                ("query_summary", models.JSONField(default=None, null=True)),
                ("feature_summary", models.JSONField(default=None, null=True)),
                ("transform_summary", models.JSONField(default=None, null=True)),
                ("device_configuration", models.JSONField(default=None, null=True)),
                ("sensor_summary", models.JSONField(default=None, null=True)),
                ("class_map", models.JSONField(default=None, null=True)),
                ("cost_summary", models.JSONField(default=None, null=True)),
                (
                    "knowledgepack_description",
                    models.JSONField(default=None, null=True),
                ),
                ("task", models.UUIDField(blank=True, null=True, unique=True)),
                ("logs", models.CharField(max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "feature_file",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="datamanager.featurefile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Knowledge Pack",
                "verbose_name_plural": "Knowledge Packs",
                "permissions": (
                    ("can_get_binaries", "Can get binary builds of knowledgepacks"),
                    ("can_get_source", "Can get source builds of knowledgepacks"),
                    ("can_get_libraries", "Can get library builds of knowledgepacks"),
                    (
                        "can_get_enterprise",
                        "Can get enterprise builds of knowledgepacks",
                    ),
                    ("can_get_developer", "Can get developer builds of knowledgepacks"),
                    (
                        "has_classification_limit",
                        "Has limited number of classifications on binary builds.",
                    ),
                    (
                        "has_sample_rate_limit",
                        "Sample rate of knowledgepack device limited to < 10kHz",
                    ),
                ),
            },
        ),
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1000)),
                ("type", models.CharField(max_length=32)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("metadata", models.BooleanField(default=False)),
                ("is_dropdown", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PipelineExecution",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("project_uuid", models.UUIDField(default=uuid.uuid4)),
                ("pipeline_uuid", models.UUIDField(default=uuid.uuid4)),
                ("task_id", models.UUIDField(default=uuid.uuid4)),
                (
                    "execution_type",
                    models.CharField(
                        choices=[
                            ("V1", "PIPE"),
                            ("V2", "AUTOML"),
                            ("V3", "RECOGNITION"),
                            ("V4", "CODEGEN"),
                            ("V5", "GRIDSEARCH"),
                            ("V6", "AUTOSEG"),
                        ],
                        max_length=2,
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("N", "STARTED"), ("S", "SUCCESS"), ("F", "FAILED")],
                        max_length=1,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=36, unique=True),
                ),
                ("capture_sample_schema", models.JSONField(default=None, null=True)),
                ("settings", models.JSONField(default=None, null=True)),
                ("optimized", models.BooleanField(default=False)),
                ("profile", models.JSONField(default=None, null=True)),
                ("plugin_config", models.JSONField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("active_pipelines", models.JSONField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                (
                    "image_file_name",
                    models.CharField(
                        default=None, max_length=1100, null=True, unique=True
                    ),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                (
                    "uaa_id",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        unique=True,
                        verbose_name="UAA Client ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=36, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("internal", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="FoundationModel",
            fields=[
                (
                    "knowledgepack_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="datamanager.knowledgepack",
                    ),
                ),
                ("description", models.CharField(max_length=255, null=True)),
                ("auxiliary_datafile", models.CharField(max_length=255, null=True)),
                ("model_profile", models.JSONField(default=None, null=True)),
                (
                    "trainable_layer_groups",
                    models.JSONField(
                        default=datamanager.models.default_trainable_layer, null=True
                    ),
                ),
            ],
            bases=("datamanager.knowledgepack",),
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="auth.user",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teammembers",
                        to="datamanager.team",
                    ),
                ),
            ],
            options={
                "verbose_name": "team member",
                "verbose_name_plural": "team members",
            },
            bases=("auth.user",),
            managers=[
                ("objects", datamanager.managers.TeamMemberManager()),
            ],
        ),
        migrations.CreateModel(
            name="Segmenter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("function", models.CharField(max_length=255, null=True)),
                ("parameters", models.JSONField(default=None, null=True)),
                ("custom", models.BooleanField(default=False)),
                ("preprocess", models.JSONField(default=None, null=True)),
                ("is_locked", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.segmenter",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "project")},
            },
        ),
        migrations.CreateModel(
            name="Sandbox",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=40, unique=True),
                ),
                ("name", models.CharField(max_length=200)),
                ("pipeline", models.JSONField(default=None, null=True)),
                ("cache_enabled", models.BooleanField(default=True)),
                ("cache", models.JSONField(null=True)),
                ("device_config", models.JSONField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("result_type", models.CharField(default="", max_length=40)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("private", models.BooleanField(default=False)),
                ("active", models.BooleanField(default=False)),
                ("hyper_params", models.JSONField(default=None, null=True)),
                ("cpu_clock_time", models.IntegerField(default=0)),
                (
                    "project",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
                ("users", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name_plural": "Sandboxes",
            },
        ),
        migrations.AddField(
            model_name="project",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="datamanager.team"
            ),
        ),
        migrations.CreateModel(
            name="LabelValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=1000)),
                ("color", models.CharField(max_length=9, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="label_values",
                        to="datamanager.label",
                    ),
                ),
            ],
            options={
                "unique_together": {("label", "value")},
            },
        ),
        migrations.AddField(
            model_name="label",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="labels",
                to="datamanager.project",
            ),
        ),
        migrations.AddField(
            model_name="knowledgepack",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="datamanager.project",
            ),
        ),
        migrations.AddField(
            model_name="knowledgepack",
            name="sandbox",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="datamanager.sandbox",
            ),
        ),
        migrations.AddField(
            model_name="featurefile",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="datamanager.project"
            ),
        ),
        migrations.CreateModel(
            name="CaptureVideo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "video_type",
                    models.CharField(
                        choices=[
                            ("U", "UPLOADED TO CLOUD"),
                            ("R", "REMOTE LOCATION"),
                            ("S", "STREAMABLE"),
                        ],
                        default="U",
                        max_length=1,
                        null=True,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("file_size", models.IntegerField(null=True)),
                ("keypoints", models.JSONField(null=True)),
                ("is_processed", models.BooleanField(default=False, null=True)),
                ("is_file_deleted", models.BooleanField(default=False, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "capture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.capture",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CaptureConfiguration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("name", models.CharField(max_length=255)),
                ("configuration", models.JSONField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "uuid"), ("name", "project")},
            },
        ),
        migrations.AddField(
            model_name="capture",
            name="capture_configuration",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="datamanager.captureconfiguration",
            ),
        ),
        migrations.AddField(
            model_name="capture",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="captures",
                to="datamanager.project",
            ),
        ),
        migrations.CreateModel(
            name="Query",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(default=uuid.uuid4, max_length=40, unique=True),
                ),
                ("name", models.CharField(max_length=200)),
                ("columns", models.CharField(max_length=5000, null=True)),
                ("metadata_columns", models.CharField(max_length=5000, null=True)),
                ("eventlabel_columns", models.CharField(max_length=5000, null=True)),
                ("metadata_filter", models.CharField(max_length=5000, null=True)),
                ("eventlabel_filter", models.CharField(max_length=5000, null=True)),
                ("label_column", models.CharField(max_length=200, null=True)),
                ("combine_labels", models.JSONField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("summary_statistics", models.JSONField(null=True)),
                ("segment_info", models.JSONField(null=True)),
                ("cache", models.JSONField(null=True)),
                ("task", models.UUIDField(blank=True, null=True, unique=True)),
                ("task_status", models.CharField(max_length=5000, null=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=False)),
                (
                    "capture_configurations",
                    models.ManyToManyField(
                        default=None, to="datamanager.CaptureConfiguration"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
                (
                    "segmenter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="datamanager.segmenter",
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "name")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="project",
            unique_together={("team", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="label",
            unique_together={("name", "project")},
        ),
        migrations.CreateModel(
            name="FeatureFileAnalysis",
            fields=[
                (
                    "featurefile_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="datamanager.featurefile",
                    ),
                ),
                (
                    "analysis_type",
                    models.CharField(
                        choices=[("P", "PCA"), ("U", "UMAP"), ("T", "TSNE")],
                        max_length=1,
                    ),
                ),
                ("params", models.JSONField(default=None, null=True)),
                (
                    "featurefile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="datamanager.featurefile",
                    ),
                ),
            ],
            bases=("datamanager.featurefile",),
        ),
        migrations.AlterUniqueTogether(
            name="featurefile",
            unique_together={("project", "name")},
        ),
        migrations.CreateModel(
            name="CaptureMetadataValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "capture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.capture",
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.label",
                    ),
                ),
                (
                    "label_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.labelvalue",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("capture", "label")},
            },
        ),
        migrations.CreateModel(
            name="CaptureLabelValue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("capture_sample_sequence_start", models.BigIntegerField()),
                ("capture_sample_sequence_end", models.BigIntegerField()),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "capture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.capture",
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.label",
                    ),
                ),
                (
                    "label_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.labelvalue",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.project",
                    ),
                ),
                (
                    "segmenter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="datamanager.segmenter",
                    ),
                ),
            ],
            options={
                "unique_together": {
                    (
                        "capture",
                        "segmenter",
                        "label",
                        "label_value",
                        "capture_sample_sequence_start",
                        "capture_sample_sequence_end",
                    )
                },
            },
        ),
        migrations.AlterUniqueTogether(
            name="capture",
            unique_together={("name", "project")},
        ),
    ]