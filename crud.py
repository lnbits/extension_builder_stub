# Description: This file contains the CRUD operations for talking to the database.

from typing import List, Optional, Union

from lnbits.db import Database
from lnbits.helpers import urlsafe_short_hash

from .models import CreateOwnerData, OwnerData

db = Database("ext_extension_builder_stub")


async def create_owner_data_table(data: CreateOwnerData) -> OwnerData:
    data.id = urlsafe_short_hash()
    await db.insert("extension_builder_stub.owner_data_table", data)
    return OwnerData(**data.dict())


async def get_owner_data_table(
    extension_builder_stub_id: str,
) -> Optional[OwnerData]:
    return await db.fetchone(
        "SELECT * FROM extension_builder_stub.owner_data_table WHERE id = :id",
        {"id": extension_builder_stub_id},
        OwnerData,
    )



async def update_owner_data_table(data: CreateOwnerData) -> OwnerData:
    await db.update("extension_builder_stub.owner_data_table", data)
    return OwnerData(**data.dict())


async def delete_owner_data_table(extension_builder_stub_id: str) -> None:
    await db.execute(
        "DELETE FROM extension_builder_stub.owner_data_table WHERE id = :id",
        {"id": extension_builder_stub_id},
    )
