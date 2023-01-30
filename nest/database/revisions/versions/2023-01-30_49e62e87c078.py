"""Add user model

Revision ID: 49e62e87c078
Revises: e539672cc329
Create Date: 2023-01-30 21:20:05.137148

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "49e62e87c078"
down_revision = "e539672cc329"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users__user",
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
        op.f("ix_users__user_email"), "users__user", ["email"], unique=True
    )
    op.create_index(
        op.f("ix_users__user_id"), "users__user", ["id"], unique=True
    )
    op.drop_index(
        "ix_nest.models.users__user_email",
        table_name="nest.models.users__user",
    )
    op.drop_index(
        "ix_nest.models.users__user_id", table_name="nest.models.users__user"
    )
    op.drop_table("nest.models.users__user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "nest.models.users__user",
        sa.Column(
            "id",
            sa.BIGINT(),
            server_default=sa.text(
                "nextval('\"nest.models.users__user_id_seq\"'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name="nest.models.users__user_pkey"),
    )
    op.create_index(
        "ix_nest.models.users__user_id",
        "nest.models.users__user",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_nest.models.users__user_email",
        "nest.models.users__user",
        ["email"],
        unique=False,
    )
    op.drop_index(op.f("ix_users__user_id"), table_name="users__user")
    op.drop_index(op.f("ix_users__user_email"), table_name="users__user")
    op.drop_table("users__user")
    # ### end Alembic commands ###
