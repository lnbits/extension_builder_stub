# Description: This file contains the CRUD operations for talking to the database.

from typing import List, Optional, Union

from lnbits.db import Database
from lnbits.helpers import urlsafe_short_hash

from .models import CreateMyExtensionData, MyExtension

db = Database("ext_extension_builder_stub")


async def create_extension_builder_stub(data: CreateMyExtensionData) -> MyExtension:
    data.id = urlsafe_short_hash()
    await db.insert("extension_builder_stub.maintable", data)
    return MyExtension(**data.dict())


async def get_extension_builder_stub(extension_builder_stub_id: str) -> Optional[MyExtension]:
    return await db.fetchone(
        "SELECT * FROM extension_builder_stub.maintable WHERE id = :id",
        {"id": extension_builder_stub_id},
        MyExtension,
    )


async def get_extension_builder_stubs(wallet_ids: Union[str, List[str]]) -> List[MyExtension]:
    if isinstance(wallet_ids, str):
        wallet_ids = [wallet_ids]
    q = ",".join([f"'{w}'" for w in wallet_ids])
    return await db.fetchall(
        f"SELECT * FROM extension_builder_stub.maintable WHERE wallet IN ({q}) ORDER BY id",
        model=MyExtension,
    )


async def update_extension_builder_stub(data: CreateMyExtensionData) -> MyExtension:
    await db.update("extension_builder_stub.maintable", data)
    return MyExtension(**data.dict())


async def delete_extension_builder_stub(extension_builder_stub_id: str) -> None:
    await db.execute(
        "DELETE FROM extension_builder_stub.maintable WHERE id = :id", {"id": extension_builder_stub_id}
    )
