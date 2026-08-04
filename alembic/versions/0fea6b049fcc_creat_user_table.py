"""creat user table

Revision ID: 0fea6b049fcc
Revises: c06ce35e4c89
Create Date: 2026-08-01 10:09:58.330911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fea6b049fcc'
down_revision: Union[str, Sequence[str], None] = 'bc82566ef814'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')))   
    pass


def downgrade() -> None:
    op.drop_table("user")
    pass
