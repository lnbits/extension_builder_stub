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
    create_owner_data,
    delete_owner_data,
    get_owner_data,
    get_owner_data_paginated,
    update_owner_data,
)
from .models import CreateOwnerData, ExtensionSettings, OwnerData, OwnerDataFilters
from .services import get_settings, update_settings

owner_data_filters = parse_filters(OwnerDataFilters)

extension_builder_stub_api_router = APIRouter()

############################# owner_data #############################


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
    "/api/v1/owner_data", status_code=HTTPStatus.CREATED
)
async def api_update_owner_data(
    data: OwnerData,
    user: User = Depends(check_user_exists),
) -> OwnerData:
    if data.user_id != user.id:
        raise HTTPException(HTTPStatus.FORBIDDEN, "You do not own this owner_data.")
    await update_owner_data(data)
    return data


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
    delete_client_data: Optional[bool] = False,
    user: User = Depends(check_user_exists),
) -> SimpleStatus:

    await delete_owner_data(user.id, owner_data_id)
    if delete_client_data is True:
        # await delete all client data associated with this owner data
        pass
    return SimpleStatus(success=True, message="Owner Data Deleted")


#  <% if settings_table.has_settings %>
################################### Settings ###########################################
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


# <% endif %>
