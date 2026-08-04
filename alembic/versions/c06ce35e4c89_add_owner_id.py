"""add owner.id

Revision ID: c06ce35e4c89
Revises: bc82566ef814
Create Date: 2026-08-01 10:06:39.160448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c06ce35e4c89'
down_revision: Union[str, Sequence[str], None] = '0fea6b049fcc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_user_fk', source_table="posts", referent_table="user", local_cols=['owner_id'],
                        remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
