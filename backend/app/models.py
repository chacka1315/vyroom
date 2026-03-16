import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

import uuid_utils
from sqlalchemy import Column, DateTime, Numeric, func
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.other_schemas import ListingStatus, ListingType, PropertyType, UserType


# --- Table models ---


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=320)
    hashed_password: str = Field(max_length=1024)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    user_type: UserType = Field(
        default=UserType.person,
        sa_column=Column(
            SAEnum(UserType, name="usertype"),
            nullable=False,
            server_default=UserType.person.value,
        ),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )

    listings: list["Listing"] = Relationship(back_populates="owner")


class Listing(ListingBase, table=True):
    __tablename__ = "listings"

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7, primary_key=True)
    price: Decimal = Field(sa_column=Column(Numeric(14, 2), nullable=False))
    listing_type: ListingType = Field(
        sa_column=Column(SAEnum(ListingType, name="listingtype"), nullable=False)
    )
    property_type: PropertyType = Field(
        sa_column=Column(SAEnum(PropertyType, name="propertytype"), nullable=False)
    )
    status: ListingStatus = Field(
        default=ListingStatus.active,
        sa_column=Column(
            SAEnum(ListingStatus, name="listingstatus"),
            nullable=False,
            server_default=ListingStatus.active.value,
        ),
    )
    owner_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

    owner: "User" = Relationship(back_populates="listings")
    location: Optional["Location"] = Relationship(back_populates="listing")
    images: list["ListingImage"] = Relationship(back_populates="listing")


class Location(LocationBase, table=True):
    __tablename__ = "locations"

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7, primary_key=True)
    listing_id: uuid.UUID = Field(foreign_key="listings.id", unique=True)

    listing: "Listing" = Relationship(back_populates="location")


class ListingImage(ListingImageBase, table=True):
    __tablename__ = "listing_images"

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7, primary_key=True)
    listing_id: uuid.UUID = Field(foreign_key="listings.id")

    listing: "Listing" = Relationship(back_populates="images")
