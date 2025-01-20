"""building

Revision ID: ea99fa8f4756
Revises: 5d554f4ef60b
Create Date: 2025-01-20 22:23:45.807788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea99fa8f4756'
down_revision: Union[str, None] = '5d554f4ef60b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('building',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('admin', sa.Column('building_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'admin', 'building', ['building_id'], ['id'])
    op.add_column('request', sa.Column('building_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'request', 'building', ['building_id'], ['id'])
    op.drop_column('request', 'building_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('building_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'request', type_='foreignkey')
    op.drop_column('request', 'building_id')
    op.drop_constraint(None, 'admin', type_='foreignkey')
    op.drop_column('admin', 'building_id')
    op.drop_table('building')
    # ### end Alembic commands ###
