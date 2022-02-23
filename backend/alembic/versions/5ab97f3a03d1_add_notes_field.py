"""Add notes field

Revision ID: 5ab97f3a03d1
Revises: 174e0bf3a047
Create Date: 2021-09-24 12:51:32.518696

"""
import sqlalchemy as sa

import src
from alembic import op

# revision identifiers, used by Alembic.
revision = "5ab97f3a03d1"
down_revision = "174e0bf3a047"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bills",
        sa.Column("notes", sa.Text(), server_default="", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bills", "notes")
    # ### end Alembic commands ###
