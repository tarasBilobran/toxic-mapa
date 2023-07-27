"""empty message

Revision ID: 9dc8e25901b8
Revises: 
Create Date: 2023-07-13 20:28:51.303005

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE public.users (
        id UUID PRIMARY KEY,
        telegram_id INT NOT NULL,
        phone TEXT,
        username TEXT,
        status TEXT NOT NULL
    );

    CREATE TABLE public.poison_report (
        id UUID PRIMARY KEY,
        reported_by UUID REFERENCES public.users (id),
        -- WKT text
        location TEXT NOT NULL,
        -- path on the local file system to files
        photos TEXT[] NOT NULL,
        status TEXT NOT NULL,
        poison_removed BOOL NOT NULL,
        created_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL 
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE public.poison_report;
    DROP TABLE public.users;
    """)
