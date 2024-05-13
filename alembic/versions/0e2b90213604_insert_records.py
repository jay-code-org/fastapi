"""insert records

Revision ID: 0e2b90213604
Revises:
Create Date: 2024-05-13 11:24:58.880084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e2b90213604'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(""" INSERT INTO categories (name)
               VALUES
               ('Cooking'),
               ('Coding'),
               ('Sports')""")

    op.execute(""" INSERT INTO roles (name)
               VALUES
               ('Admin'),
               ('User')""")

    op.execute(""" INSERT INTO statuses (name)
               VALUES
               ('New'),
               ('Completed'),
               ('Suspended'),
               ('Active'),
               ('Blocked'),
               ('Deleted'),
               ('Terminated')""")
    pass


def downgrade() -> None:
    pass
