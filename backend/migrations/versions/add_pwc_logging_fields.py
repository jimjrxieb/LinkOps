"""Add PwC-aligned logging fields to Log model

Revision ID: pwc_logging_fields
Revises: 504629267976
Create Date: 2024-01-15 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "pwc_logging_fields"
down_revision = "504629267976"
branch_labels = None
depends_on = None


def upgrade():
    # Add PwC-aligned audit fields to logs table
    op.add_column("logs", sa.Column("solution_path", sa.Text(), nullable=True))
    op.add_column("logs", sa.Column("error_outcome", sa.Text(), nullable=True))
    op.add_column(
        "logs",
        sa.Column("sanitized", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "logs",
        sa.Column("approved", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.add_column(
        "logs",
        sa.Column(
            "auto_approved", sa.Boolean(), nullable=False, server_default="false"
        ),
    )
    op.add_column("logs", sa.Column("compliance_tags", sa.Text(), nullable=True))

    # Create indexes for performance
    op.create_index(op.f("ix_logs_sanitized"), "logs", ["sanitized"], unique=False)
    op.create_index(op.f("ix_logs_approved"), "logs", ["approved"], unique=False)


def downgrade():
    # Remove indexes
    op.drop_index(op.f("ix_logs_approved"), table_name="logs")
    op.drop_index(op.f("ix_logs_sanitized"), table_name="logs")

    # Remove columns
    op.drop_column("logs", "compliance_tags")
    op.drop_column("logs", "auto_approved")
    op.drop_column("logs", "approved")
    op.drop_column("logs", "sanitized")
    op.drop_column("logs", "error_outcome")
    op.drop_column("logs", "solution_path")
