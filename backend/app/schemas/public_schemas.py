import uuid
from datetime import datetime

from fastapi_users import schemas as fu_schemas

from app.models import ListingBase, ListingImageBase, LocationBase
from app.schemas.other_schemas import UserType


# --- User ---

class UserPublic(fu_schemas.BaseUser[uuid.UUID]):
    full_name: str | None = None
    phone_number: str | None = None
    avatar_url: str | None = None
    user_type: UserType
    created_at: datetime | None = None


# --- Location ---

class LocationPublic(LocationBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


# --- ListingImage ---

class ListingImagePublic(ListingImageBase):
    id: uuid.UUID

    model_config = {"from_attributes": True}


# --- Listing ---

class ListingPublic(ListingBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ListingDetail(ListingPublic):
    location: LocationPublic | None = None
    images: list[ListingImagePublic] = []
    owner: UserPublic
