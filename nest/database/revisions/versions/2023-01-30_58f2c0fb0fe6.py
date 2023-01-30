"""Add user model

Revision ID: 58f2c0fb0fe6
Revises: 49e62e87c078
Create Date: 2023-01-30 21:20:28.280991

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "58f2c0fb0fe6"
down_revision = "49e62e87c078"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users_user",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_user_email"), "users_user", ["email"], unique=True
    )
    op.create_index(
        op.f("ix_users_user_id"), "users_user", ["id"], unique=True
    )
    op.drop_index("ix_users__user_email", table_name="users__user")
    op.drop_index("ix_users__user_id", table_name="users__user")
    op.drop_table("users__user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users__user",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "first_name", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "last_name", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "password", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="users__user_pkey"),
    )
    op.create_index("ix_users__user_id", "users__user", ["id"], unique=False)
    op.create_index(
        "ix_users__user_email", "users__user", ["email"], unique=False
    )
    op.drop_index(op.f("ix_users_user_id"), table_name="users_user")
    op.drop_index(op.f("ix_users_user_email"), table_name="users_user")
    op.drop_table("users_user")
    # ### end Alembic commands ###
