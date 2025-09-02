
from pydantic import BaseModel
from typing import Optional


class CreateOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

class OwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""

class CreateClientData(BaseModel):
    """<< cancel_comment >>
    <% for field in client_table.editable_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class ClientData(BaseModel):
    """<< cancel_comment >>
    <% for field in client_table.all_fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
