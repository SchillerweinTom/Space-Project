"""Image save

Revision ID: 795562f5cf34
Revises: 6c226ed0ee27
Create Date: 2025-01-20 14:19:00.238864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795562f5cf34'
down_revision = '6c226ed0ee27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('destination', sa.String(length=50), nullable=True),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('route')
    # ### end Alembic commands ###
