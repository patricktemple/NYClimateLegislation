from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Text,
    TypeDecorator,
    sql,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP as _TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as _UUID
from sqlalchemy.orm import relationship

from .app import app
from .utils import now

db = SQLAlchemy(app)


class UUID(TypeDecorator):
    impl = _UUID(as_uuid=True)


class TIMESTAMP(TypeDecorator):
    impl = _TIMESTAMP(timezone=True)


class Bill(db.Model):
    __tablename__ = "bills"

    # These are all auto-populated by the API:
    id = Column(Integer, primary_key=True)
    file = Column(Text, nullable=False)  # e.g. Int 2317-2021
    name = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    status = Column(Text)
    body = Column(Text)

    intro_date = Column(TIMESTAMP, nullable=False)

    @property
    def tracked(self):
        return True

    # Data we track
    notes = Column(Text, nullable=False, server_default="")
    nickname = Column(Text, nullable=False, server_default="")

    sponsorships = relationship(
        "BillSponsorship", back_populates="bill", cascade="all, delete"
    )
    attachments = relationship(
        "BillAttachment", back_populates="bill", cascade="all, delete"
    )


class Legislator(db.Model):
    __tablename__ = "legislators"

    # These come from the API
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    term_start = Column(TIMESTAMP)
    term_end = Column(TIMESTAMP)
    email = Column(Text)
    district_phone = Column(Text)
    legislative_phone = Column(Text)

    sponsorships = relationship("BillSponsorship", back_populates="legislator")

    borough = Column(Text)
    website = Column(Text)

    # These are added by our static data
    twitter = Column(Text)  # exclude the @ symbol
    party = Column(Text)

    # Track our own info on the bill.
    notes = Column(Text)


class BillSponsorship(db.Model):
    __tablename__ = "bill_sponsorships"

    bill_id = Column(
        Integer, ForeignKey("bills.id"), nullable=False, primary_key=True
    )
    bill = relationship(
        "Bill", back_populates="sponsorships", order_by="Bill.name"
    )

    legislator_id = Column(
        Integer, ForeignKey("legislators.id"), nullable=False, primary_key=True
    )
    legislator = relationship(
        "Legislator", back_populates="sponsorships", order_by="Legislator.name"
    )


# TODO: UUIDs for some PKs?
class BillAttachment(db.Model):
    __tablename__ = "bill_attachments"

    id = Column(Integer, primary_key=True)
    bill_id = Column(
        Integer, ForeignKey("bills.id"), nullable=False, index=True
    )
    bill = relationship("Bill", back_populates="attachments")

    name = Column(Text)
    url = Column(Text, nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)

    email = Column(
        Text, index=True, nullable=False, unique=True
    )  # always lowercase
    name = Column(Text)

    login_links = relationship(
        "LoginLink", back_populates="user", cascade="all, delete"
    )

    # The "root" user can never be deleted.
    can_be_deleted = Column(Boolean, nullable=False, server_default=sql.true())

    __table_args__ = (
        CheckConstraint(
            "email = lower(email)", name="check_email_is_lowercase"
        ),
    )


class LoginLink(db.Model):
    __tablename__ = "login_links"

    user_id = Column(UUID, ForeignKey(User.id), nullable=False)

    token = Column(Text, nullable=False, primary_key=True)

    expires_at = Column(TIMESTAMP, nullable=False)

    created_at = Column(TIMESTAMP, nullable=False, default=now)

    user = relationship("User", back_populates="login_links")

    # TODO: Consider only allowing these links to be used once. Better security
    # in case of leaked browser URL, but worse UX.
