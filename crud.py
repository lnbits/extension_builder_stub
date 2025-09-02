# Description: This file contains the CRUD operations for talking to the database.

from typing import Optional

from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import CreateOwnerData, OwnerData, OwnerDataFilters

db = Database("ext_extension_builder_stub")


async def create_owner_data(data: CreateOwnerData) -> OwnerData:
    owner_data = OwnerData(**data.dict(), id=urlsafe_short_hash())
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


async def update_owner_data(user_id: str, data: OwnerData):
    # todo: user_id
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
