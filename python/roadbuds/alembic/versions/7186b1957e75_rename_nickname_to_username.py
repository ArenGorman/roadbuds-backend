"""rename nickname to username

Revision ID: 7186b1957e75
Revises: b984e56c64a5
Create Date: 2026-01-13 18:54:36.933659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7186b1957e75'
down_revision: Union[str, Sequence[str], None] = 'b984e56c64a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename nickname column to username in users table."""
    # Rename the column (preserves data and constraints)
    op.alter_column(
        'users',
        'nickname',
        new_column_name='username',
        schema='roadbuds'
    )


def downgrade() -> None:
    """Revert username column back to nickname."""
    # Rename back to nickname
    op.alter_column(
        'users',
        'username',
        new_column_name='nickname',
        schema='roadbuds'
    )
