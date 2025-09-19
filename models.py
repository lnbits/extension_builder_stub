from datetime import datetime, timezone

from lnbits.db import FilterModel
from pydantic import BaseModel, Field


########################### Owner Data ############################
class CreateOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_data.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

    extra: dict = {}


class OwnerData(BaseModel):
    id: str
    user_id: str
    """<< cancel_comment >>
    <% for field in owner_data.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OwnerDataFilters(FilterModel):
    __search_fields__ = [
        """<< cancel_comment >>
        <% for field in owner_data.search_fields %>"<< field >>",<% endfor%>
        << cancel_comment >>"""
    ]

    __sort_fields__ = [
        """<< cancel_comment >>
        <% for field in owner_data.search_fields %>"<< field >>",
        <% endfor%>
        << cancel_comment >>"""
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


################################# Client Data ###########################


class CreateClientData(BaseModel):
    """<< cancel_comment >>
    <% for field in client_data.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class ClientData(BaseModel):
    id: str
    owner_data_id: str
    """<< cancel_comment >>
    <% for field in client_data.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# <% if generate_payment_logic %> << cancel_comment >>
class ClientDataPaymentRequest(BaseModel):
    client_data_id: str
    payment_hash: str
    payment_request: str


# <% endif %> << cancel_comment >>


class ClientDataFilters(FilterModel):
    __search_fields__ = [
        """<< cancel_comment >>
        <% for field in client_data.search_fields %>"<< field >>",<% endfor%>
        << cancel_comment >>"""
    ]

    __sort_fields__ = [
        """<< cancel_comment >>
        <% for field in client_data.search_fields %>"<< field >>",
        <% endfor%>
        << cancel_comment >>"""
        "created_at",
        "updated_at",
    ]

    created_at: datetime | None
    updated_at: datetime | None


#  <% if settings_data.enabled %> << cancel_comment >>
############################ Settings #############################
class ExtensionSettings(BaseModel):
    """<< cancel_comment >>
    <% for field in settings_data.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def is_admin_only(cls) -> bool:
        return bool("<< settings_data.is_admin_settings_only >>" == "True")


class UserExtensionSettings(ExtensionSettings):
    id: str


# <% endif %> << cancel_comment >>
