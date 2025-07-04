"""init

Revision ID: d0f79de30e4c
Revises:
Create Date: 2025-06-21 04:09:23.404025

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d0f79de30e4c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.Column("changes", sa.Text(), nullable=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"], unique=False
    )
    op.create_index(
        op.f("ix_audit_logs_entity_type"), "audit_logs", ["entity_type"], unique=False
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_table(
        "links",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("screenshot_path", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_links_id"), "links", ["id"], unique=False)
    op.create_index(op.f("ix_links_url"), "links", ["url"], unique=False)
    op.create_table(
        "logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent", sa.String(length=100), nullable=False),
        sa.Column("task_id", sa.String(length=100), nullable=False),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_logs_agent"), "logs", ["agent"], unique=False)
    op.create_index(op.f("ix_logs_task_id"), "logs", ["task_id"], unique=False)
    op.create_table(
        "orbs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orbs_category"), "orbs", ["category"], unique=False)
    op.create_index(op.f("ix_orbs_name"), "orbs", ["name"], unique=False)
    op.create_table(
        "system_metrics",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("metric_name", sa.String(length=100), nullable=False),
        sa.Column("metric_value", sa.String(length=255), nullable=False),
        sa.Column("metric_unit", sa.String(length=20), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_system_metrics_id"), "system_metrics", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_system_metrics_metric_name"),
        "system_metrics",
        ["metric_name"],
        unique=False,
    )
    op.create_table(
        "whis_queue",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("task_id", sa.String(length=255), nullable=False),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("agent", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_whis_queue_status"), "whis_queue", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_whis_queue_task_id"), "whis_queue", ["task_id"], unique=False
    )
    op.create_table(
        "runes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("orb_id", sa.UUID(), nullable=False),
        sa.Column("script_path", sa.String(length=500), nullable=True),
        sa.Column("script_content", sa.Text(), nullable=True),
        sa.Column("language", sa.String(length=50), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("feedback_score", sa.Float(), nullable=True),
        sa.Column("feedback_count", sa.Integer(), nullable=True),
        sa.Column("last_feedback", sa.Text(), nullable=True),
        sa.Column("is_flagged", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["orb_id"],
            ["orbs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_runes_language"), "runes", ["language"], unique=False)
    op.create_index(op.f("ix_runes_orb_id"), "runes", ["orb_id"], unique=False)
    op.create_index(op.f("ix_runes_task_id"), "runes", ["task_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_runes_task_id"), table_name="runes")
    op.drop_index(op.f("ix_runes_orb_id"), table_name="runes")
    op.drop_index(op.f("ix_runes_language"), table_name="runes")
    op.drop_table("runes")
    op.drop_index(op.f("ix_whis_queue_task_id"), table_name="whis_queue")
    op.drop_index(op.f("ix_whis_queue_status"), table_name="whis_queue")
    op.drop_table("whis_queue")
    op.drop_index(op.f("ix_system_metrics_metric_name"), table_name="system_metrics")
    op.drop_index(op.f("ix_system_metrics_id"), table_name="system_metrics")
    op.drop_table("system_metrics")
    op.drop_index(op.f("ix_orbs_name"), table_name="orbs")
    op.drop_index(op.f("ix_orbs_category"), table_name="orbs")
    op.drop_table("orbs")
    op.drop_index(op.f("ix_logs_task_id"), table_name="logs")
    op.drop_index(op.f("ix_logs_agent"), table_name="logs")
    op.drop_table("logs")
    op.drop_index(op.f("ix_links_url"), table_name="links")
    op.drop_index(op.f("ix_links_id"), table_name="links")
    op.drop_table("links")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_type"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_id"), table_name="audit_logs")
    op.drop_table("audit_logs")
    # ### end Alembic commands ###
