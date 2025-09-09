# Description: This file contains the extensions API endpoints.
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from lnbits.core.models import SimpleStatus, User
from lnbits.db import Filters, Page
from lnbits.decorators import (
    check_user_exists,
    parse_filters,
)
from lnbits.helpers import generate_filter_params_openapi

from .crud import (
    create_client_data,
    create_owner_data,
    delete_client_data,
    delete_owner_data,
    get_client_data_by_id,
    get_client_data_paginated,
    get_owner_data,
    get_owner_data_ids_by_user,
    get_owner_data_paginated,
    update_client_data,
    update_owner_data,
)
from .models import (
    ClientData,
    ClientDataFilters,
    CreateClientData,
    CreateOwnerData,
    ExtensionSettings,
    OwnerData,
    OwnerDataFilters,
)
from .services import get_settings, update_settings

owner_data_filters = parse_filters(OwnerDataFilters)
client_data_filters = parse_filters(ClientDataFilters)

extension_builder_stub_api_router = APIRouter()


############################# Owner Data #############################
@extension_builder_stub_api_router.post(
    "/api/v1/owner_data", status_code=HTTPStatus.CREATED
)
async def api_create_owner_data(
    data: CreateOwnerData,
    user: User = Depends(check_user_exists),
) -> OwnerData:
    # todo: user_id
    owner_data = await create_owner_data(user.id, data)
    return owner_data


@extension_builder_stub_api_router.put(
    "/api/v1/owner_data/{owner_data_id}", status_code=HTTPStatus.CREATED
)
async def api_update_owner_data(
    owner_data_id: str,
    data: CreateOwnerData,
    user: User = Depends(check_user_exists),
) -> OwnerData:
    owner_data = await get_owner_data(user.id, owner_data_id)
    if not owner_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Owner Data not found.")
    if owner_data.user_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this owner data.")
    owner_data = await update_owner_data(OwnerData(**owner_data.dict(), **data.dict()))
    return owner_data


@extension_builder_stub_api_router.get(
    "/api/v1/owner_data/paginated",
    name="Owner Data List",
    summary="get paginated list of owner_data",
    response_description="list of owner_data",
    openapi_extra=generate_filter_params_openapi(OwnerDataFilters),
    response_model=Page[OwnerData],
)
async def api_get_owner_data_paginated(
    user: User = Depends(check_user_exists),
    filters: Filters = Depends(owner_data_filters),
) -> Page[OwnerData]:

    return await get_owner_data_paginated(
        user_id=user.id,
        filters=filters,
    )


@extension_builder_stub_api_router.get(
    "/api/v1/owner_data/{owner_data_id}",
    name="Get OwnerData",
    summary="Get the owner_data with this id.",
    response_description="An owner_data or 404 if not found",
    response_model=OwnerData,
)
async def api_get_owner_data(
    owner_data_id: str,
    user: User = Depends(check_user_exists),
) -> OwnerData:

    owner_data = await get_owner_data(user.id, owner_data_id)
    if not owner_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "OwnerData not found.")

    return owner_data


@extension_builder_stub_api_router.delete(
    "/api/v1/owner_data/{owner_data_id}",
    name="Delete Owner Data",
    summary="Delete the owner_data " "and optionally all its associated client_data.",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_owner_data(
    owner_data_id: str,
    clear_client_data: Optional[bool] = False,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    await delete_owner_data(user.id, owner_data_id)
    if clear_client_data is True:
        # await delete all client data associated with this owner data
        pass
    return SimpleStatus(success=True, message="Owner Data Deleted")


############################# Client Data #############################
@extension_builder_stub_api_router.post(
    "/api/v1/client_data/{owner_data_id}",
    name="Create Client Data",
    summary="Create new client data for the specified owner data.",
    response_description="The created client data.",
    response_model=ClientData,
    status_code=HTTPStatus.CREATED,
)
async def api_create_client_data(
    owner_data_id: str,
    data: CreateClientData,
    user: User = Depends(check_user_exists),
) -> ClientData:
    owner_data = await get_owner_data(user.id, owner_data_id)
    if not owner_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Owner Data not found.")

    client_data = await create_client_data(owner_data_id, data)
    return client_data


@extension_builder_stub_api_router.put(
    "/api/v1/client_data/{client_data_id}",
    name="Update Client Data",
    summary="Update the client_data with this id.",
    response_description="The updated client data.",
    response_model=ClientData,
)
async def api_update_client_data(
    client_data_id: str,
    data: CreateClientData,
    user: User = Depends(check_user_exists),
) -> ClientData:
    client_data = await get_client_data_by_id(client_data_id)
    if not client_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Client Data not found.")

    owner_data = await get_owner_data(user.id, client_data.owner_data_id)
    if not owner_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Owner Data not found.")

    client_data = await update_client_data(
        ClientData(**client_data.dict(), **data.dict())
    )
    return client_data


@extension_builder_stub_api_router.get(
    "/api/v1/client_data/paginated",
    name="Client Data List",
    summary="get paginated list of client_data",
    response_description="list of client_data",
    openapi_extra=generate_filter_params_openapi(ClientDataFilters),
    response_model=Page[ClientData],
)
async def api_get_client_data_paginated(
    user: User = Depends(check_user_exists),
    filters: Filters = Depends(client_data_filters),
) -> Page[ClientData]:

    owner_data_ids = await get_owner_data_ids_by_user(user.id)
    return await get_client_data_paginated(
        owner_data_ids=owner_data_ids,
        filters=filters,
    )


@extension_builder_stub_api_router.get(
    "/api/v1/client_data/{client_data_id}",
    name="Get Client Data",
    summary="Get the client data with this id.",
    response_description="An client data or 404 if not found",
    response_model=ClientData,
)
async def api_get_client_data(
    client_data_id: str,
    user: User = Depends(check_user_exists),
) -> ClientData:

    client_data = await get_client_data_by_id(client_data_id)
    if not client_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "ClientData not found.")
    owner_data = await get_owner_data(user.id, client_data.owner_data_id)
    if not owner_data:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Owner Data deleted for this Client Data."
        )

    return client_data


@extension_builder_stub_api_router.delete(
    "/api/v1/client_data/{client_data_id}",
    name="Delete Client Data",
    summary="Delete the client_data",
    response_description="The status of the deletion.",
    response_model=SimpleStatus,
)
async def api_delete_client_data(
    client_data_id: str,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    client_data = await get_client_data_by_id(client_data_id)
    if not client_data:
        raise HTTPException(HTTPStatus.NOT_FOUND, "ClientData not found.")
    owner_data = await get_owner_data(user.id, client_data.owner_data_id)
    if not owner_data:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Owner Data deleted for this Client Data."
        )

    await delete_client_data(owner_data.id, client_data_id)
    return SimpleStatus(success=True, message="Client Data Deleted")


#  <% if settings_table.has_settings %> << cancel_comment >>
############################ Settings #############################
@extension_builder_stub_api_router.get(
    "/api/v1/settings",
    name="Get Settings",
    summary="Get the settings for the current user.",
    response_description="The settings or 404 if not found",
    response_model=ExtensionSettings,
)
async def api_get_settings(
    user: User = Depends(check_user_exists),
) -> ExtensionSettings:
    user_id = "admin" if ExtensionSettings.is_admin_only() else user.id
    return await get_settings(user_id)


@extension_builder_stub_api_router.put(
    "/api/v1/settings",
    name="Update Settings",
    summary="Update the settings for the current user.",
    response_description="The updated settings.",
    response_model=ExtensionSettings,
)
async def api_update_extension_settings(
    data: ExtensionSettings,
    user: User = Depends(check_user_exists),
) -> ExtensionSettings:
    if ExtensionSettings.is_admin_only() and not user.admin:
        raise HTTPException(
            HTTPStatus.FORBIDDEN,
            "Only admins can update settings.",
        )
    user_id = "admin" if ExtensionSettings.is_admin_only() else user.id
    return await update_settings(user_id, data)


# <% endif %> << cancel_comment >>
