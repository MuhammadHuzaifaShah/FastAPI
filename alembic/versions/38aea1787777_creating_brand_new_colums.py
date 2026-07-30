"""Creating brand new Colums

Revision ID: 38aea1787777
Revises: 19c257eb4792
Create Date: 2026-07-29 02:23:01.160630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38aea1787777'
down_revision: Union[str, Sequence[str], None] = '19c257eb4792'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
