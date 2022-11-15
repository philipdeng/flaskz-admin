"""add license

Revision ID: 92ad21293203
Revises: 5656baaceae2
Create Date: 2022-09-16 18:01:45.106622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92ad21293203'
down_revision = '5656baaceae2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sys_licenses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('license', sa.Text(), nullable=False),
    sa.Column('user', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('start_date', sa.String(length=255), nullable=True),
    sa.Column('end_date', sa.String(length=255), nullable=True),
    sa.Column('created_user', sa.String(length=32), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('license')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sys_licenses')
    # ### end Alembic commands ###