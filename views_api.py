# Description: This file contains the extensions API endpoints.

from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from lnbits.core.crud import get_user
from lnbits.core.models import WalletTypeInfo
from lnbits.core.services import create_invoice
from lnbits.decorators import require_admin_key, require_invoice_key
from starlette.exceptions import HTTPException

from .crud import (
    create_extension_builder_stub,
    delete_extension_builder_stub,
    get_extension_builder_stub,
    get_extension_builder_stubs,
    update_extension_builder_stub,
)
from .helpers import lnurler
from .models import CreateMyExtensionData, CreatePayment, MyExtension

extension_builder_stub_api_router = APIRouter()

# Note: we add the lnurl params to returns so the links
# are generated in the MyExtension model in models.py

## Get all the records belonging to the user


@extension_builder_stub_api_router.get("/api/v1/myex")
async def api_extension_builder_stubs(
    req: Request,  # Withoutthe lnurl stuff this wouldnt be needed
    wallet: WalletTypeInfo = Depends(require_invoice_key),
) -> list[MyExtension]:
    wallet_ids = [wallet.wallet.id]
    user = await get_user(wallet.wallet.user)
    wallet_ids = user.wallet_ids if user else []
    extension_builder_stubs = await get_extension_builder_stubs(wallet_ids)

    # Populate lnurlpay and lnurlwithdraw for each instance.
    # Without the lnurl stuff this wouldnt be needed.
    for myex in extension_builder_stubs:
        myex.lnurlpay = lnurler(myex.id, "extension_builder_stub.api_lnurl_pay", req)
        myex.lnurlwithdraw = lnurler(
            myex.id, "extension_builder_stub.api_lnurl_withdraw", req
        )

    return extension_builder_stubs


## Get a single record


@extension_builder_stub_api_router.get(
    "/api/v1/myex/{extension_builder_stub_id}",
    dependencies=[Depends(require_invoice_key)],
)
async def api_extension_builder_stub(
    extension_builder_stub_id: str, req: Request
) -> MyExtension:
    myex = await get_extension_builder_stub(extension_builder_stub_id)
    if not myex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )
    # Populate lnurlpay and lnurlwithdraw.
    # Without the lnurl stuff this wouldnt be needed.
    myex.lnurlpay = lnurler(myex.id, "extension_builder_stub.api_lnurl_pay", req)
    myex.lnurlwithdraw = lnurler(
        myex.id, "extension_builder_stub.api_lnurl_withdraw", req
    )

    return myex


## Create a new record


@extension_builder_stub_api_router.post("/api/v1/myex", status_code=HTTPStatus.CREATED)
async def api_extension_builder_stub_create(
    req: Request,  # Withoutthe lnurl stuff this wouldnt be needed
    data: CreateMyExtensionData,
    wallet: WalletTypeInfo = Depends(require_admin_key),
) -> MyExtension:
    myex = await create_extension_builder_stub(data)

    # Populate lnurlpay and lnurlwithdraw.
    # Withoutthe lnurl stuff this wouldnt be needed.
    myex.lnurlpay = lnurler(myex.id, "extension_builder_stub.api_lnurl_pay", req)
    myex.lnurlwithdraw = lnurler(
        myex.id, "extension_builder_stub.api_lnurl_withdraw", req
    )

    return myex


## update a record


@extension_builder_stub_api_router.put("/api/v1/myex/{extension_builder_stub_id}")
async def api_extension_builder_stub_update(
    req: Request,  # Withoutthe lnurl stuff this wouldnt be needed
    data: CreateMyExtensionData,
    extension_builder_stub_id: str,
    wallet: WalletTypeInfo = Depends(require_admin_key),
) -> MyExtension:
    myex = await get_extension_builder_stub(extension_builder_stub_id)
    if not myex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )

    if wallet.wallet.id != myex.wallet:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not your MyExtension."
        )

    for key, value in data.dict().items():
        setattr(myex, key, value)

    myex = await update_extension_builder_stub(data)

    # Populate lnurlpay and lnurlwithdraw.
    # Without the lnurl stuff this wouldnt be needed.
    myex.lnurlpay = lnurler(myex.id, "extension_builder_stub.api_lnurl_pay", req)
    myex.lnurlwithdraw = lnurler(
        myex.id, "extension_builder_stub.api_lnurl_withdraw", req
    )

    return myex


## Delete a record


@extension_builder_stub_api_router.delete("/api/v1/myex/{extension_builder_stub_id}")
async def api_extension_builder_stub_delete(
    extension_builder_stub_id: str, wallet: WalletTypeInfo = Depends(require_admin_key)
):
    myex = await get_extension_builder_stub(extension_builder_stub_id)

    if not myex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )

    if myex.wallet != wallet.wallet.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not your MyExtension."
        )

    await delete_extension_builder_stub(extension_builder_stub_id)
    return


# ANY OTHER ENDPOINTS YOU NEED

## This endpoint creates a payment


@extension_builder_stub_api_router.post(
    "/api/v1/myex/payment", status_code=HTTPStatus.CREATED
)
async def api_extension_builder_stub_create_invoice(data: CreatePayment) -> dict:
    extension_builder_stub = await get_extension_builder_stub(
        data.extension_builder_stub_id
    )

    if not extension_builder_stub:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )

    # we create a payment and add some tags,
    # so tasks.py can grab the payment once its paid

    payment = await create_invoice(
        wallet_id=extension_builder_stub.wallet,
        amount=data.amount,
        memo=(
            f"{data.memo} to {extension_builder_stub.name}"
            if data.memo
            else f"{extension_builder_stub.name}"
        ),
        extra={
            "tag": "extension_builder_stub",
            "amount": data.amount,
        },
    )

    return {"payment_hash": payment.payment_hash, "payment_request": payment.bolt11}
