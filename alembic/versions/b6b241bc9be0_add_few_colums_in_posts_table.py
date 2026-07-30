"""Add few colums in posts table

Revision ID: b6b241bc9be0
Revises: f18b740554ba
Create Date: 2026-07-31 02:28:00.361663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6b241bc9be0'
down_revision: Union[str, Sequence[str], None] = 'f18b740554ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
                sa.Column('published',sa.Boolean(),server_default='TRUE',nullable=False)
    )
    op.add_column('posts',
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published'),
    op.drop_column('posts','created_at')
    pass
