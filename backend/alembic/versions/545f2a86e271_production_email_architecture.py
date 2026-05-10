"""production email architecture

Revision ID: 545f2a86e271
Revises:
Create Date: 2026-05-11 00:08:40.348554
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '545f2a86e271'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # SAFE COLUMN RENAME
    op.alter_column(
        'email_logs',
        'email',
        new_column_name='user_email'
    )

    # SAFE INDEX CREATION
    op.create_index(
        op.f('ix_email_logs_id'),
        'email_logs',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    # REMOVE INDEX
    op.drop_index(
        op.f('ix_email_logs_id'),
        table_name='email_logs'
    )

    # RENAME COLUMN BACK
    op.alter_column(
        'email_logs',
        'user_email',
        new_column_name='email'
    )