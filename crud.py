# Description: This file contains the CRUD operations for talking to the database.

from typing import Optional

from lnbits.db import Database, Filters, Page
from lnbits.helpers import urlsafe_short_hash

from .models import (
    ClientData,
    ClientDataFilters,
    CreateClientData,
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


########################### Owner Data ############################
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


async def get_owner_data_by_id(
    owner_data_id: str,
) -> Optional[OwnerData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.owner_data
            WHERE id = :id
        """,
        {"id": owner_data_id},
        OwnerData,
    )


async def get_owner_data_ids_by_user(
    user_id: str,
) -> list[str]:
    rows: list[dict] = await db.fetchall(
        """
            SELECT DISTINCT id FROM extension_builder_stub.owner_data
            WHERE user_id = :user_id
        """,
        {"user_id": user_id},
    )

    return [row["id"] for row in rows]


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


async def update_owner_data(data: OwnerData) -> OwnerData:
    await db.update("extension_builder_stub.owner_data", data)
    return data


async def delete_owner_data(user_id: str, owner_data_id: str) -> None:
    await db.execute(
        """
            DELETE FROM extension_builder_stub.owner_data
            WHERE id = :id AND user_id = :user_id
        """,
        {"id": owner_data_id, "user_id": user_id},
    )


################################# Client Data ###########################


async def create_client_data(owner_data_id: str, data: CreateClientData) -> ClientData:
    client_data = ClientData(
        **data.dict(), id=urlsafe_short_hash(), owner_data_id=owner_data_id
    )
    await db.insert("extension_builder_stub.client_data", client_data)
    return client_data


async def get_client_data(
    owner_data_id: str,
    client_data_id: str,
) -> Optional[ClientData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.client_data
            WHERE id = :id AND owner_data_id = :owner_data_id
        """,
        {"id": client_data_id, "owner_data_id": owner_data_id},
        ClientData,
    )


async def get_client_data_by_id(
    client_data_id: str,
) -> Optional[ClientData]:
    return await db.fetchone(
        """
            SELECT * FROM extension_builder_stub.client_data
            WHERE id = :id
        """,
        {"id": client_data_id},
        ClientData,
    )


# async def get_public_client_data(
#     client_data_id: str,
# ) -> Optional[PublicClientData]:
#     return await db.fetchone(
#         """
#             SELECT * FROM extension_builder_stub.client_data
#             WHERE id = :id
#         """,
#         {"id": client_data_id},
#         PublicClientData,
#     )


async def get_client_data_paginated(
    owner_data_ids: Optional[list[str]] = None,
    filters: Optional[Filters[ClientDataFilters]] = None,
) -> Page[ClientData]:
    where = []
    values = {}

    if owner_data_ids:
        id_clause = []
        for i, item_id in enumerate(owner_data_ids):
            # owner_data_ids are not user input, but DB entries, so this is safe
            owner_data_id = f"owner_data_id__{i}"
            id_clause.append(f"owner_data_id = :{owner_data_id}")
            values[owner_data_id] = item_id
        where.append(" OR ".join(id_clause))

    return await db.fetch_page(
        "SELECT * FROM extension_builder_stub.client_data",
        where=where,
        values=values,
        filters=filters,
        model=ClientData,
    )


async def update_client_data(data: ClientData) -> ClientData:
    await db.update("extension_builder_stub.client_data", data)
    return data


async def delete_client_data(owner_data_id: str, client_data_id: str) -> None:
    await db.execute(
        """
            DELETE FROM extension_builder_stub.client_data
            WHERE id = :id AND owner_data_id = :owner_data_id
        """,
        {"id": client_data_id, "owner_data_id": owner_data_id},
    )


#  <% if settings_table.has_settings %> << cancel_comment >>
############################ Settings #############################
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


async def update_extension_settings(user_id: str, data: ExtensionSettings):
    settings = UserExtensionSettings(**data.dict(), id=user_id)
    await db.update("extension_builder_stub.extension_settings", settings)


# <% endif %> << cancel_comment >>
