# Description: This file contains the CRUD operations for talking to the database.

from typing import Optional

from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import CreateOwnerData, OwnerData

db = Database("ext_extension_builder_stub")


async def create_owner_data_table(data: CreateOwnerData) -> OwnerData:
    owner_data_table = OwnerData(**data.dict(), id=urlsafe_short_hash())
    await db.insert("extension_builder_stub.owner_data_table", owner_data_table)
    return owner_data_table


async def get_owner_data_table(
    user_id: str,
    owner_data_table_id: str,
) -> Optional[OwnerData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.owner_data_table
            WHERE id = :id AND user_id = :user_id""",
        {"id": owner_data_table_id, "user_id": user_id},
        OwnerData,
    )


async def get_owner_data_table_paginated(
    user_id: Optional[str] = None,
    filters: Optional[Filters[OwnerDataFilters]] = None,
) -> Page[OwnerData]:
    where = []
    values = {}
    if user_id:
        where.append("user_id = :user_id")
        values["user_id"] = user_id

    return await db.fetch_page(
        "SELECT * FROM extension_builder_stub.owner_data_table",
        where=where,
        values=values,
        filters=filters,
        model=OwnerData,
    )


async def update_owner_data_table(user_id: str, data: OwnerData):
    # todo: user_id
    await db.update("extension_builder_stub.owner_data_table", data)


async def delete_owner_data_table(user_id: str, owner_data_table_id: str) -> None:
    # todo: user_id
    await db.execute(
        """
            DELETE FROM extension_builder_stub.owner_data_table
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_table_id, "user_id": user_id},
    )
