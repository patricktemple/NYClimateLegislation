from uuid import uuid4

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import column_property, foreign, relationship, remote

from ..bill.models import AssemblyBill, Bill, CityBill, SenateBill
from ..models import TIMESTAMP, UUID, db
from ..person.models import AssemblyMember, CouncilMember, Person, Senator


class CitySponsorship(db.Model):
    __tablename__ = "city_sponsorships"

    id = Column(UUID, primary_key=True, default=uuid4)

    bill_id = Column(
        UUID,
        ForeignKey("city_bills.bill_id"),
        nullable=False,
        index=True,
    )
    city_bill = relationship(
        CityBill,
        back_populates="sponsorships",
    )

    council_member_id = Column(
        UUID,
        ForeignKey("council_members.person_id"),
        nullable=False,
        index=True,
    )
    council_member = relationship(
        CouncilMember,
        back_populates="sponsorships",
    )

    sponsor_sequence = Column(Integer, nullable=False)

    # The timestamp when we first saw this sponsorship in the bill's list.
    # This is a proxy for when the sponsor actually signed on to the bill.
    # Note that when we first start tracking a bill, it may already have sponsorships
    # and we don't know the date that those were added. We leave added_at as null,
    # in that case, and only fill this in for sponsorships that were added later on.
    added_at = Column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint(
            "bill_id", "council_member_id", name="_bill_council_member_unique"
        ),
    )


CitySponsorship.bill = relationship(
    Bill,
    primaryjoin=remote(Bill.id) == foreign(CitySponsorship.bill_id),
    viewonly=True,
)
CitySponsorship.person = relationship(
    Person,
    primaryjoin=remote(Person.id)
    == foreign(CitySponsorship.council_member_id),
    viewonly=True,
)


class SenateSponsorship(db.Model):
    __tablename__ = "senate_sponsorships"

    id = Column(UUID, primary_key=True, default=uuid4)

    senate_bill_id = Column(
        UUID, ForeignKey(SenateBill.bill_id), nullable=False, index=True
    )
    senate_bill = relationship(
        SenateBill,
        back_populates="sponsorships",
    )

    senator_id = Column(
        UUID, ForeignKey(Senator.person_id), nullable=False, index=True
    )
    senator = relationship(Senator, back_populates="sponsorships")

    # TODO: Add sponsor_sequence like we have with city, if needed


class AssemblySponsorship(db.Model):
    __tablename__ = "assembly_sponsorships"

    id = Column(UUID, primary_key=True, default=uuid4)

    assembly_bill_id = Column(
        UUID, ForeignKey(AssemblyBill.bill_id), nullable=False, index=True
    )
    assembly_bill = relationship(
        AssemblyBill,
        back_populates="sponsorships",
    )

    assembly_member_id = Column(
        UUID, ForeignKey(AssemblyMember.person_id), nullable=False, index=True
    )
    assembly_member = relationship(
        AssemblyMember, back_populates="sponsorships"
    )

    # TODO: Add sponsor_sequence like we have with city, if needed


# This may be inefficient because it loads this on every bill even if these fields aren't needed
CityBill.sponsor_count = column_property(
    select(func.count(CitySponsorship.id))
    .where(CitySponsorship.bill_id == CityBill.bill_id)
    .correlate_except(CitySponsorship)
    .scalar_subquery()
)
SenateBill.sponsor_count = column_property(
    select(func.count(SenateSponsorship.id))
    .where(SenateSponsorship.senate_bill_id == SenateBill.bill_id)
    .correlate_except(SenateSponsorship)
    .scalar_subquery()
)
AssemblyBill.sponsor_count = column_property(
    select(func.count(AssemblySponsorship.id))
    .where(AssemblySponsorship.assembly_bill_id == AssemblyBill.bill_id)
    .correlate_except(AssemblySponsorship)
    .scalar_subquery()
)
