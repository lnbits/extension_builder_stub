from datetime import datetime

from lnbits.db import FilterModel
from pydantic import BaseModel


class CreateOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class OwnerData(BaseModel):
    id: str
    user_id: str
    """<< cancel_comment >>
    <% for field in owner_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


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
