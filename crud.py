# Description: This file contains the CRUD operations for talking to the database.

from typing import Optional

from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    CreateOwnerData,
    OwnerData,
    OwnerDataFilters,
    PublicOwnerData,
)

#  <% if settings_table.has_settings %> << cancel_comment >>
from .models import ExtensionSettings as ExtensionSettings
from .models import UserExtensionSettings as UserExtensionSettings

# <% endif %> << cancel_comment >>

db = Database("ext_extension_builder_stub")


async def create_owner_data(user_id: str, data: CreateOwnerData) -> OwnerData:
    owner_data = OwnerData(**data.dict(), id=urlsafe_short_hash(), user_id=user_id)
    await db.insert("extension_builder_stub.owner_data", owner_data)
    return owner_data


async def get_owner_data(
    user_id: str,
    owner_data_id: str,
) -> Optional[OwnerData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.owner_data
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_id, "user_id": user_id},
        OwnerData,
    )


async def get_public_owner_data(
    owner_data_id: str,
) -> Optional[PublicOwnerData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.owner_data
            WHERE id = :id
        """,
        {"id": owner_data_id},
        PublicOwnerData,
    )


async def get_owner_data_paginated(
    user_id: Optional[str] = None,
    filters: Optional[Filters[OwnerDataFilters]] = None,
) -> Page[OwnerData]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM extension_builder_stub.owner_data",
        where=where,
        values=values,
        filters=filters,
        model=OwnerData,
    )


async def update_owner_data(data: OwnerData):
    await db.update("extension_builder_stub.owner_data", data)


async def delete_owner_data(user_id: str, owner_data_id: str) -> None:
    # todo: user_id
    await db.execute(
        """
            DELETE FROM extension_builder_stub.owner_data
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_id, "user_id": user_id},
    )


#  <% if settings_table.has_settings %>
################################### Settings ###########################################
async def create_extension_settings(
    user_id: str, data: ExtensionSettings
) -> ExtensionSettings:
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.insert("extension_builder_stub.extension_settings", settings)
    return settings


async def get_extension_settings(
    user_id: str,
) -> Optional[ExtensionSettings]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.extension_settings
            WHERE id = :user_id
        """,
        {"user_id": user_id},
        ExtensionSettings,
    )


async def update_extension_settings(data: ExtensionSettings):
    await db.update("extension_builder_stub.extension_settings", data)


# <% endif %>
