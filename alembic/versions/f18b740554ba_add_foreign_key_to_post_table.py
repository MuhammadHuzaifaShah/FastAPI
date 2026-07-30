"""Add foreign key to post table

Revision ID: f18b740554ba
Revises: eff54bf143ee
Create Date: 2026-07-31 02:08:30.812182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f18b740554ba'
down_revision: Union[str, Sequence[str], None] = 'eff54bf143ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
