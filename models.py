from typing import Optional

from pydantic import BaseModel


class CreateOwnerData(BaseModel):
    """<< cancel_comment >>
    <% for field in owner_table.fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class CreateClientData(BaseModel):
    """<< cancel_comment >>
    <% for field in client_table.fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""
