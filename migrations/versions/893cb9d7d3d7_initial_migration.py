"""Initial migration

Revision ID: 893cb9d7d3d7
Revises: 
Create Date: 2025-01-28 10:29:48.670805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '893cb9d7d3d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('country', sa.String(length=150), nullable=True),
    sa.Column('state', sa.String(length=150), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('student_name', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('phone', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('country', sa.String(length=150), nullable=True),
    sa.Column('state', sa.String(length=150), nullable=True),
    sa.Column('church_branch', sa.String(length=150), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_super_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('pledged_amount', sa.Float(), nullable=True),
    sa.Column('pledge_currency', sa.String(length=3), nullable=True),
    sa.Column('paid_status', sa.Boolean(), nullable=True),
    sa.Column('medal', sa.String(length=100), nullable=True),
    sa.Column('partner_since', sa.Integer(), nullable=True),
    sa.Column('donation_date', sa.Date(), nullable=False),
    sa.Column('has_received_onboarding_email', sa.Boolean(), nullable=True),
    sa.Column('has_received_onboarding_sms', sa.Boolean(), nullable=True),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('donations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=50), nullable=True),
    sa.Column('donation_date', sa.Date(), nullable=False),
    sa.Column('payment_type', sa.String(length=20), nullable=False),
    sa.Column('receipt_filename', sa.String(length=255), nullable=True),
    sa.Column('amount_paid', sa.Float(), nullable=False),
    sa.Column('pledged_amount', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('paid_status', sa.Boolean(), nullable=True),
    sa.Column('medal', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pledges',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('pledged_amount', sa.Numeric(), nullable=True),
    sa.Column('pledge_currency', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pledges')
    op.drop_table('donations')
    op.drop_table('user')
    op.drop_table('invoices')
    op.drop_table('attendance')
    op.drop_table('tenants')
    # ### end Alembic commands ###
