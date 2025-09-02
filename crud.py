# Description: This file contains the CRUD operations for talking to the database.

from typing import Optional

from lnbits.db import Database
from lnbits.helpers import urlsafe_short_hash

from .models import CreateOwnerData, OwnerData

db = Database("ext_extension_builder_stub")


async def create_owner_data_table(data: CreateOwnerData) -> OwnerData:
    owner_data_table = OwnerData(**data.dict(), id=urlsafe_short_hash())
    await db.insert("extension_builder_stub.owner_data_table", owner_data_table)
    return owner_data_table


async def get_owner_data_table(
    owner_data_table_id: str,
) -> Optional[OwnerData]:
    return await db.fetchone(
        "SELECT * FROM extension_builder_stub.owner_data_table WHERE id = :id",
        {"id": owner_data_table_id},
        OwnerData,
    )


async def update_owner_data_table(data: OwnerData):
    await db.update("extension_builder_stub.owner_data_table", data)


async def delete_owner_data_table(owner_data_table_id: str) -> None:
    await db.execute(
        "DELETE FROM extension_builder_stub.owner_data_table WHERE id = :id",
        {"id": owner_data_table_id},
    )
