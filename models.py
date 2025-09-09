from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Owner Data ############################
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
    id: str
    """<< cancel_comment >>
    <% for field in owner_table.public_fields %><< field >>
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


################################# Client Data ###########################


class CreateClientData(BaseModel):
    owner_data_id: str
    """<< cancel_comment >>
    <% for field in client_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class ClientData(BaseModel):
    id: str
    owner_data_id: str
    """<< cancel_comment >>
    <% for field in client_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PublicClientData(BaseModel):
    id: str
    """<< cancel_comment >>
    <% for field in client_table.public_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class ClientDataFilters(FilterModel):
    __search_fields__ = [
        """<< cancel_comment >>
        <% for field in client_table.search_fields %>"<< field >>",<% endfor%>
        << cancel_comment >>"""
    ]

    __sort_fields__ = [
        """<< cancel_comment >>
        <% for field in client_table.search_fields %>"<< field >>",
        <% endfor%>
        << cancel_comment >>"""
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


#  <% if settings_table.has_settings %> << cancel_comment >>
############################ Settings #############################
class ExtensionSettings(BaseModel):
    """<< cancel_comment >>
    <% for field in settings_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("<< settings_table.is_admin_settings_only >>" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str


# <% endif %> << cancel_comment >>
