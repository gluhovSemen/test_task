"""init

Revision ID: 8a68c73ff6f2
Revises: 
Create Date: 2023-10-18 19:37:14.784245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8a68c73ff6f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add code to create the user and auth_token tables
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('surname', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('eth_address', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.CheckConstraint("password ~* '[0-9]' AND password ~* '[A-Z]'", name="password_format_check"),
                    sa.CheckConstraint("CHAR_LENGTH(password) >= 8", name="password_length_check"),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('auth_token',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('token', sa.String(), nullable=True),  # Set nullable=True
                    sa.Column('user_id', sa.Integer(), nullable=True),  # Define the foreign key
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_auth_token_user_id'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    # Add code to drop the tables
    op.drop_table('auth_token')
    op.drop_table('user')
