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
