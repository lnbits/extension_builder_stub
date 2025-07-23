# Description: Extensions that use LNURL usually have a few endpoints in views_lnurl.py.

from http import HTTPStatus
from typing import Optional

import shortuuid
from fastapi import APIRouter, Query, Request
from lnbits.core.services import create_invoice, pay_invoice
from loguru import logger

from .crud import get_extension_builder_stub

#################################################
########### A very simple LNURLpay ##############
# https://github.com/lnurl/luds/blob/luds/06.md #
#################################################
#################################################

extension_builder_stub_lnurl_router = APIRouter()


@extension_builder_stub_lnurl_router.get(
    "/api/v1/lnurl/pay/{extension_builder_stub_id}",
    status_code=HTTPStatus.OK,
    name="extension_builder_stub.api_lnurl_pay",
)
async def api_lnurl_pay(
    request: Request,
    extension_builder_stub_id: str,
):
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    if not extension_builder_stub:
        return {"status": "ERROR", "reason": "No extension_builder_stub found"}
    return {
        "callback": str(
            request.url_for(
                "extension_builder_stub.api_lnurl_pay_callback",
                extension_builder_stub_id=extension_builder_stub_id,
            )
        ),
        "maxSendable": extension_builder_stub.lnurlpayamount * 1000,
        "minSendable": extension_builder_stub.lnurlpayamount * 1000,
        "metadata": '[["text/plain", "' + extension_builder_stub.name + '"]]',
        "tag": "payRequest",
    }


@extension_builder_stub_lnurl_router.get(
    "/api/v1/lnurl/paycb/{extension_builder_stub_id}",
    status_code=HTTPStatus.OK,
    name="extension_builder_stub.api_lnurl_pay_callback",
)
async def api_lnurl_pay_cb(
    request: Request,
    extension_builder_stub_id: str,
    amount: int = Query(...),
):
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    logger.debug(extension_builder_stub)
    if not extension_builder_stub:
        return {"status": "ERROR", "reason": "No extension_builder_stub found"}

    memo = extension_builder_stub.name
    payment = await create_invoice(
        wallet_id=extension_builder_stub.wallet,
        amount=int(amount / 1000),
        memo=memo,
        unhashed_description=f'[["text/plain", "{memo}"]]'.encode(),
        extra={
            "tag": "Extension Builder Stub",
            "extension_builder_stubId": extension_builder_stub_id,
            "extra": request.query_params.get("amount"),
        },
    )
    return {
        "pr": payment.bolt11,
        "routes": [],
        "successAction": {
            "tag": "message",
            "message": f"Paid {memo}",
        },
    }


#################################################
######## A very simple LNURLwithdraw ############
# https://github.com/lnurl/luds/blob/luds/03.md #
#################################################
## withdraw is unlimited, look at withdraw ext ##
## for more advanced withdraw options          ##
#################################################


@extension_builder_stub_lnurl_router.get(
    "/api/v1/lnurl/withdraw/{extension_builder_stub_id}",
    status_code=HTTPStatus.OK,
    name="extension_builder_stub.api_lnurl_withdraw",
)
async def api_lnurl_withdraw(
    request: Request,
    extension_builder_stub_id: str,
):
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    if not extension_builder_stub:
        return {"status": "ERROR", "reason": "No extension_builder_stub found"}
    k1 = shortuuid.uuid(name=extension_builder_stub.id)
    return {
        "tag": "withdrawRequest",
        "callback": str(
            request.url_for(
                "extension_builder_stub.api_lnurl_withdraw_callback",
                extension_builder_stub_id=extension_builder_stub_id,
            )
        ),
        "k1": k1,
        "defaultDescription": extension_builder_stub.name,
        "maxWithdrawable": extension_builder_stub.lnurlwithdrawamount * 1000,
        "minWithdrawable": extension_builder_stub.lnurlwithdrawamount * 1000,
    }


@extension_builder_stub_lnurl_router.get(
    "/api/v1/lnurl/withdrawcb/{extension_builder_stub_id}",
    status_code=HTTPStatus.OK,
    name="extension_builder_stub.api_lnurl_withdraw_callback",
)
async def api_lnurl_withdraw_cb(
    extension_builder_stub_id: str,
    pr: Optional[str] = None,
    k1: Optional[str] = None,
):
    assert k1, "k1 is required"
    assert pr, "pr is required"
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    if not extension_builder_stub:
        return {"status": "ERROR", "reason": "No extension_builder_stub found"}

    k1_check = shortuuid.uuid(name=extension_builder_stub.id)
    if k1_check != k1:
        return {"status": "ERROR", "reason": "Wrong k1 check provided"}

    await pay_invoice(
        wallet_id=extension_builder_stub.wallet,
        payment_request=pr,
        max_sat=int(extension_builder_stub.lnurlwithdrawamount * 1000),
        extra={
            "tag": "Extension Builder Stub",
            "extension_builder_stubId": extension_builder_stub_id,
            "lnurlwithdraw": True,
        },
    )
    return {"status": "OK"}
