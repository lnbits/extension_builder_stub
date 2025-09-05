from .crud import (
    create_extension_settings,
    get_extension_settings,
    update_extension_settings,
)
from .models import ExtensionSettings


#  <% if settings_table.has_settings %>
async def get_settings(user_id: str) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    return settings


async def update_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    return await update_extension_settings(data)


# <% endif %>
