"""update to enum

Revision ID: d031458797ed
Revises: bac38132e14e
Create Date: 2025-04-10 20:23:15.508921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd031458797ed'
down_revision: Union[str, None] = 'bac38132e14e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_id', table_name='user')
    op.drop_table('user')
    op.execute("ALTER TYPE source ADD VALUE 'event'")
    op.execute("ALTER TYPE status ADD VALUE 'contacted'")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('updated_at', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    # ### end Alembic commands ###
