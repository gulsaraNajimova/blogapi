"""Add tsvector column to blogs

Revision ID: b3f2ecef7d45
Revises: 
Create Date: 2023-11-30 22:41:46.451502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

# revision identifiers, used by Alembic.
revision: str = 'b3f2ecef7d45'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blogs', sa.Column('tsvector_column', TSVECTOR(), nullable=True))
    op.create_index('ix_blogs_tsvector_column', 'blogs', ['tsvector_column'], unique=False, postgresql_using='gin')


def downgrade() -> None:
    op.drop_index('ix_blogs_tsvector_column', 'blogs')
    op.drop_column('blogs', 'tsvector_column')

