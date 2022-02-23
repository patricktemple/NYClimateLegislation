"""Refactor for state

Revision ID: f84b802082d4
Revises: a33750368a20
Create Date: 2021-12-26 09:56:48.664575

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import src
from alembic import op

# revision identifiers, used by Alembic.
revision = "f84b802082d4"
down_revision = "a33750368a20"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bills_2",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column(
            "type", sa.Enum("CITY", "STATE", name="billtype"), nullable=False
        ),
        sa.Column("notes", sa.Text(), server_default="", nullable=False),
        sa.Column("nickname", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "twitter_search_terms", postgresql.ARRAY(sa.Text()), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "persons",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column("phone", sa.Text(), nullable=True),
        sa.Column("twitter", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "COUNCIL_MEMBER",
                "ASSEMBLY_MEMBER",
                "SENATOR",
                "STAFFER",
                name="persontype",
            ),
            nullable=False,
        ),
        sa.Column("party", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "assembly_members",
        sa.Column("person_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
        ),
        sa.PrimaryKeyConstraint("person_id"),
    )
    op.create_table(
        "bill_attachments_2",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["bills_2.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bill_attachments_2_bill_id"),
        "bill_attachments_2",
        ["bill_id"],
        unique=False,
    )
    op.create_table(
        "city_bills",
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("city_bill_id", sa.Integer(), nullable=False),
        sa.Column("file", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column(
            "intro_date", src.models.TIMESTAMP(timezone=True), nullable=False
        ),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("active_version", sa.Text(), nullable=False),
        sa.Column("council_body", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["bills_2.id"],
        ),
        sa.PrimaryKeyConstraint("bill_id"),
    )
    op.create_index(
        op.f("ix_city_bills_city_bill_id"),
        "city_bills",
        ["city_bill_id"],
        unique=True,
    )
    op.create_table(
        "council_members",
        sa.Column("person_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("city_council_person_id", sa.Integer(), nullable=False),
        sa.Column(
            "term_start", src.models.TIMESTAMP(timezone=True), nullable=True
        ),
        sa.Column(
            "term_end", src.models.TIMESTAMP(timezone=True), nullable=True
        ),
        sa.Column("legislative_phone", sa.Text(), nullable=True),
        sa.Column("borough", sa.Text(), nullable=True),
        sa.Column("website", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
        ),
        sa.PrimaryKeyConstraint("person_id"),
    )
    op.create_index(
        op.f("ix_council_members_city_council_person_id"),
        "council_members",
        ["city_council_person_id"],
        unique=True,
    )
    op.create_table(
        "power_hours_2",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("spreadsheet_url", sa.Text(), nullable=False),
        sa.Column("spreadsheet_id", sa.Text(), nullable=False),
        sa.Column(
            "created_at", src.models.TIMESTAMP(timezone=True), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["bills_2.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_power_hours_2_bill_id"),
        "power_hours_2",
        ["bill_id"],
        unique=False,
    )
    op.create_table(
        "senators",
        sa.Column("person_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
        ),
        sa.PrimaryKeyConstraint("person_id"),
    )
    op.create_table(
        "staffers_2",
        sa.Column("person_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("boss_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["boss_id"],
            ["persons.id"],
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["persons.id"],
        ),
        sa.PrimaryKeyConstraint("person_id"),
    )
    op.create_index(
        op.f("ix_staffers_2_boss_id"), "staffers_2", ["boss_id"], unique=False
    )
    op.create_table(
        "state_bills",
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["bills_2.id"],
        ),
        sa.PrimaryKeyConstraint("bill_id"),
    )
    op.create_table(
        "assembly_bill_versions",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=True),
        sa.Column("version_name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["state_bills.bill_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assembly_bill_versions_bill_id"),
        "assembly_bill_versions",
        ["bill_id"],
        unique=False,
    )
    op.create_table(
        "city_sponsorships",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "council_member_id", src.models.UUID(as_uuid=True), nullable=False
        ),
        sa.Column("sponsor_sequence", sa.Integer(), nullable=False),
        sa.Column(
            "added_at", src.models.TIMESTAMP(timezone=True), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["city_bills.bill_id"],
        ),
        sa.ForeignKeyConstraint(
            ["council_member_id"],
            ["council_members.person_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "bill_id", "council_member_id", name="_bill_council_member_unique"
        ),
    )
    op.create_index(
        op.f("ix_city_sponsorships_bill_id"),
        "city_sponsorships",
        ["bill_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_city_sponsorships_council_member_id"),
        "city_sponsorships",
        ["council_member_id"],
        unique=False,
    )
    op.create_table(
        "senate_bill_versions",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column("bill_id", src.models.UUID(as_uuid=True), nullable=True),
        sa.Column("version_name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["bill_id"],
            ["state_bills.bill_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_senate_bill_versions_bill_id"),
        "senate_bill_versions",
        ["bill_id"],
        unique=False,
    )
    op.create_table(
        "assembly_sponsorships",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "assembly_version_id",
            src.models.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "assembly_member_id", src.models.UUID(as_uuid=True), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["assembly_member_id"],
            ["assembly_members.person_id"],
        ),
        sa.ForeignKeyConstraint(
            ["assembly_version_id"],
            ["assembly_bill_versions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_assembly_sponsorships_assembly_member_id"),
        "assembly_sponsorships",
        ["assembly_member_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_assembly_sponsorships_assembly_version_id"),
        "assembly_sponsorships",
        ["assembly_version_id"],
        unique=False,
    )
    op.create_table(
        "senate_sponsorships",
        sa.Column("id", src.models.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "senate_version_id", src.models.UUID(as_uuid=True), nullable=False
        ),
        sa.Column("senator_id", src.models.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["senate_version_id"],
            ["senate_bill_versions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["senator_id"],
            ["senators.person_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_senate_sponsorships_senate_version_id"),
        "senate_sponsorships",
        ["senate_version_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_senate_sponsorships_senator_id"),
        "senate_sponsorships",
        ["senator_id"],
        unique=False,
    )
    op.drop_index("ix_power_hours_bill_id", table_name="power_hours")
    op.drop_table("power_hours")
    op.drop_table("bill_sponsorships")
    op.drop_table("staffers")
    op.drop_index("ix_bill_attachments_bill_id", table_name="bill_attachments")
    op.drop_table("bill_attachments")
    op.drop_table("bills")
    op.drop_table("legislators")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "bill_attachments",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "bill_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("url", sa.TEXT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["bill_id"], ["bills.id"], name="bill_attachments_bill_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="bill_attachments_pkey"),
    )
    op.create_index(
        "ix_bill_attachments_bill_id",
        "bill_attachments",
        ["bill_id"],
        unique=False,
    )
    op.create_table(
        "staffers",
        sa.Column(
            "id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("title", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("email", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("phone", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "legislator_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("twitter", sa.TEXT(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["legislator_id"],
            ["legislators.id"],
            name="staffers_legislator_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id", name="staffers_pkey"),
    )
    op.create_table(
        "bill_sponsorships",
        sa.Column(
            "bill_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "legislator_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "added_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "sponsor_sequence",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["bill_id"], ["bills.id"], name="bill_sponsorships_bill_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["legislator_id"],
            ["legislators.id"],
            name="bill_sponsorships_legislator_id_fkey",
        ),
        sa.PrimaryKeyConstraint(
            "bill_id", "legislator_id", name="bill_sponsorships_pkey"
        ),
    )
    op.create_table(
        "legislators",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column(
            "term_start",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "term_end",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("email", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "district_phone", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "legislative_phone", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column("borough", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("website", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("notes", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("twitter", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("party", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="legislators_pkey"),
    )
    op.create_table(
        "bills",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('bills_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("file", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("title", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("status", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("body", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "intro_date",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.TEXT(),
            server_default=sa.text("''::text"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "nickname",
            sa.TEXT(),
            server_default=sa.text("''::text"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "twitter_search_terms",
            postgresql.ARRAY(sa.TEXT()),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="bills_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "power_hours",
        sa.Column(
            "id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "bill_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("title", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "spreadsheet_url", sa.TEXT(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "spreadsheet_id", sa.TEXT(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["bill_id"], ["bills.id"], name="power_hours_bill_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="power_hours_pkey"),
    )
    op.create_index(
        "ix_power_hours_bill_id", "power_hours", ["bill_id"], unique=False
    )
    op.drop_index(
        op.f("ix_senate_sponsorships_senator_id"),
        table_name="senate_sponsorships",
    )
    op.drop_index(
        op.f("ix_senate_sponsorships_senate_version_id"),
        table_name="senate_sponsorships",
    )
    op.drop_table("senate_sponsorships")
    op.drop_index(
        op.f("ix_assembly_sponsorships_assembly_version_id"),
        table_name="assembly_sponsorships",
    )
    op.drop_index(
        op.f("ix_assembly_sponsorships_assembly_member_id"),
        table_name="assembly_sponsorships",
    )
    op.drop_table("assembly_sponsorships")
    op.drop_index(
        op.f("ix_senate_bill_versions_bill_id"),
        table_name="senate_bill_versions",
    )
    op.drop_table("senate_bill_versions")
    op.drop_index(
        op.f("ix_city_sponsorships_council_member_id"),
        table_name="city_sponsorships",
    )
    op.drop_index(
        op.f("ix_city_sponsorships_bill_id"), table_name="city_sponsorships"
    )
    op.drop_table("city_sponsorships")
    op.drop_index(
        op.f("ix_assembly_bill_versions_bill_id"),
        table_name="assembly_bill_versions",
    )
    op.drop_table("assembly_bill_versions")
    op.drop_table("state_bills")
    op.drop_index(op.f("ix_staffers_2_boss_id"), table_name="staffers_2")
    op.drop_table("staffers_2")
    op.drop_table("senators")
    op.drop_index(op.f("ix_power_hours_2_bill_id"), table_name="power_hours_2")
    op.drop_table("power_hours_2")
    op.drop_index(
        op.f("ix_council_members_city_council_person_id"),
        table_name="council_members",
    )
    op.drop_table("council_members")
    op.drop_index(op.f("ix_city_bills_city_bill_id"), table_name="city_bills")
    op.drop_table("city_bills")
    op.drop_index(
        op.f("ix_bill_attachments_2_bill_id"), table_name="bill_attachments_2"
    )
    op.drop_table("bill_attachments_2")
    op.drop_table("assembly_members")
    op.drop_table("persons")
    op.drop_table("bills_2")
    # ### end Alembic commands ###
