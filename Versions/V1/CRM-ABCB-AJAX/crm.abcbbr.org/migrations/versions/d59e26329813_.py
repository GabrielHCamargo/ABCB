"""empty message

Revision ID: d59e26329813
Revises: 
Create Date: 2023-02-26 09:31:01.693953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd59e26329813'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('benefits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('nb', sa.String(length=255), nullable=False),
    sa.Column('cpf', sa.String(length=255), nullable=True),
    sa.Column('dib', sa.String(length=255), nullable=True),
    sa.Column('species', sa.String(length=255), nullable=True),
    sa.Column('salary', sa.String(length=255), nullable=True),
    sa.Column('bank', sa.String(length=255), nullable=True),
    sa.Column('agency', sa.String(length=255), nullable=True),
    sa.Column('account', sa.String(length=255), nullable=True),
    sa.Column('discounted', sa.String(length=255), nullable=True),
    sa.Column('start_date', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nb')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('documents', sa.Boolean(), nullable=True),
    sa.Column('cpf', sa.String(length=255), nullable=False),
    sa.Column('rg', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('birth_date', sa.String(length=255), nullable=True),
    sa.Column('mother', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('neighborhood', sa.String(length=255), nullable=True),
    sa.Column('cep', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('upload_date', sa.String(length=255), nullable=True),
    sa.Column('update_date', sa.String(length=255), nullable=True),
    sa.Column('obs', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation', sa.String(length=255), nullable=True),
    sa.Column('result', sa.String(length=255), nullable=True),
    sa.Column('error', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exporteds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('referent', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('hour', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.String(length=255), nullable=True),
    sa.Column('period', sa.String(length=255), nullable=True),
    sa.Column('folder', sa.String(length=255), nullable=True),
    sa.Column('requester', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('finance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('nb', sa.String(length=255), nullable=True),
    sa.Column('month', sa.String(length=255), nullable=True),
    sa.Column('discount', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('importeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('referent', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('hour', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.String(length=255), nullable=True),
    sa.Column('folder', sa.String(length=255), nullable=True),
    sa.Column('sender', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reporteds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('referent', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('hour', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.String(length=255), nullable=True),
    sa.Column('folder', sa.String(length=255), nullable=True),
    sa.Column('sender', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('hierarchy', sa.String(length=255), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('reporteds')
    op.drop_table('importeds')
    op.drop_table('finance')
    op.drop_table('exporteds')
    op.drop_table('codes')
    op.drop_table('clients')
    op.drop_table('benefits')
    # ### end Alembic commands ###
