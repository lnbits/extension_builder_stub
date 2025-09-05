from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


class CreateOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

    extra: dict = {}


class OwnerData(BaseModel):
    id: str
    user_id: str
    """<< cancel_comment >>
    <% for field in owner_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PublicOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.public_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


# class CreateClientData(BaseModel):
#     """<< cancel_comment >>
#     <% for field in client_table.editable_fields %><< field >>
#     <% endfor%>
#     << cancel_comment >>"""


class ClientData(BaseModel):
    """<< cancel_comment >>
    <% for field in client_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class OwnerDataFilters(FilterModel):
    __search_fields__ = [
        """<< cancel_comment >>
        <% for field in owner_table.search_fields %>"<< field >>",<% endfor%>
        << cancel_comment >>"""
    ]

    __sort_fields__ = [
        """<< cancel_comment >>
        <% for field in owner_table.search_fields %>"<< field >>",
        <% endfor%>
        << cancel_comment >>"""
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


#  <% if settings_table.has_settings %>
################################### Settings ###########################################
class ExtensionSettings(BaseModel):
    """<< cancel_comment >>
    <% for field in settings_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("<< settings_table.is_admin_settings_only >>" == "True")


class UserExtensionSettings(ExtensionSettings):
    user_id: str


# <% endif %>
