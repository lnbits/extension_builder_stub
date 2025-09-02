# Description: Pydantic data models dictate what is passed between frontend and backend.

from typing import Optional

from pydantic import BaseModel


class CreateXxxOwnerXxxData(BaseModel):
    """<< cancel_comment >>
    <% for field in table.fields %><< field >>
    <% endfor%>
    << cancel_comment >>"""


class MyExtension(BaseModel):
    id: str
    name: str
    lnurlpayamount: int
    lnurlwithdrawamount: int
    wallet: str
    total: int
    lnurlpay: Optional[str] = ""
    lnurlwithdraw: Optional[str] = ""


class CreatePayment(BaseModel):
    extension_builder_stub_id: str
    amount: int
    memo: str
