from decimal import Decimal
from typing import Literal

from fastapi.datastructures import Default
from fastapi_users import schemas as fu_schemas
from sqlmodel import SQLModel, Field
from sqlalchemy import DECIMAL, Column

from app.schemas.other_schemas import (
    ListingStatus,
    ListingType,
    PropertyType,
    UserType,
    PropertySubType,
)


# --- User ---
class UserBase(SQLModel):
    full_name: str = Field(max_length=100)
    user_type: UserType = Field(default=UserType.person)
    phone_number: str = Field(max_length=20)
    whatsapp_number: str | None = Field(default=None, max_length=20)
    facebook_link: str | None = Field(default=None, max_length=255)
    instagram_link: str | None = Field(default=None, max_length=255)
    webpage_link: str | None = Field(default=None, max_length=255)
    avatar_url: str | None = None
    avatar_public_id: str | None = None


class UserCreate(fu_schemas.BaseUserCreate, UserBase):
    pass


class UserUpdate(fu_schemas.BaseUserUpdate, UserBase):
    pass


# --- Listing ---
class ListingBase(SQLModel):
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=300)

    price: Decimal = Field(ge=0, sa_column=Column(DECIMAL, nullable=False))
    currency: str = Field(default="USD", max_length=10)
    listing_type: ListingType
    property_type: PropertyType
    property_sub_type: PropertySubType | None = None
    status: ListingStatus = Field(default=ListingStatus.active)
    bedrooms: int = Field(default=0, ge=0)
    bathrooms: int = Field(default=0, ge=0)

    country: str
    city: str
    municipality: str | None = Field(default=None, max_length=50)
    neighborhood: str = Field(min_length=2, max_length=50)
    area_m2: Decimal | None = Field(default=None, ge=0, sa_column=Column(DECIMAL))
    latitude: Decimal | None = Field(default=None, sa_column=Column(DECIMAL))
    longitude: Decimal | None = Field(default=None, sa_column=Column(DECIMAL))


class ListingCreate(ListingBase):
    pass


class ListingUpdate(ListingBase):
    pass


# --- Listing images ---
class ListingMediaBase(SQLModel):
    url: str = Field(max_length=500)
    type: Literal["image", "video"]
    public_id: str
    order: int = Field(default=0, ge=0)


class ListingImageCreate(ListingMediaBase):
    pass


# ---- Leads -------
class LeadBase(SQLModel):
    country: str = Field(max_length=100)
    city: str = Field(max_length=100)
    neighborhood: str = Field(default=None, max_length=100)


class Lead(SQLModel, table=True):
    listing_type: ListingType
    property_type: PropertyType

    city: str
    district: str
    neighborhood: str | None = None

    budget_min: int | None = None
    budget_max: int | None = None

    message: str | None = None
