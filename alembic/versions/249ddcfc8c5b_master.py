"""master

Revision ID: 249ddcfc8c5b
Revises: c23c9bb56756
Create Date: 2025-12-02 14:24:29.627290

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '249ddcfc8c5b'
down_revision: Union[str, None] = 'c23c9bb56756'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    now = datetime.utcnow()
    op.bulk_insert(
        sa.table(
            'users',
            sa.column('id', sa.Integer),
            sa.column('username', sa.String),
            sa.column('email', sa.String),
            sa.column('hashed_password', sa.String),
            sa.column('created_at', sa.DateTime),
            sa.column('updated_at', sa.DateTime),
        ),
        [
            {
                'id': 1,
                'username': 'テストユーザー',
                'email': 'test@test.com',
                'hashed_password': '$argon2id$v=19$m=65536,t=3,p=4$8H5PyTmnVGqNESJkbC2ldA$yQiC0thqdq8u9YeVTQg8JIB4RmulXZRZFys3S/3eMaY',
                'created_at': now,
                'updated_at': now,
            },
        ],
    )


def downgrade() -> None:
    pass


