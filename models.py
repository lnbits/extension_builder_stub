# Description: Pydantic data models dictate what is passed between frontend and backend.

from typing import Optional

from pydantic import BaseModel


class CreateMyExtensionData(BaseModel):
    id: Optional[str] = ""
    name: str
    lnurlpayamount: int
    lnurlwithdrawamount: int
    wallet: str
    total: int = 0
    """ [[ cancel_comment ]]
    [% for field in fields %]
    [[ field.name ]]: Optional[[[ field.type ]]] = None[% endfor %]
    [[ cancel_comment ]] """


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
