import asyncio

from lnbits.core.models import Payment
from lnbits.core.services import websocket_updater
from lnbits.tasks import register_invoice_listener

from .crud import get_extension_builder_stub, update_extension_builder_stub
from .models import CreateMyExtensionData

#######################################
########## RUN YOUR TASKS HERE ########
#######################################

# The usual task is to listen to invoices related to this extension


async def wait_for_paid_invoices():
    invoice_queue = asyncio.Queue()
    register_invoice_listener(invoice_queue, "ext_extension_builder_stub")
    while True:
        payment = await invoice_queue.get()
        await on_invoice_paid(payment)


# Do somethhing when an invoice related top this extension is paid


async def on_invoice_paid(payment: Payment) -> None:
    if payment.extra.get("tag") != "Extension Builder Stub":
        return

    extension_builder_stub_id = payment.extra.get("extension_builder_stubId")
    assert extension_builder_stub_id, "extension_builder_stubId not set in invoice"
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    assert extension_builder_stub, "MyExtension does not exist"

    # update something in the db
    if payment.extra.get("lnurlwithdraw"):
        total = extension_builder_stub.total - payment.amount
    else:
        total = extension_builder_stub.total + payment.amount

    extension_builder_stub.total = total
    await update_extension_builder_stub(
        CreateMyExtensionData(**extension_builder_stub.dict())
    )

    # here we could send some data to a websocket on
    # wss://<your-lnbits>/api/v1/ws/<extension_builder_stub_id> and then listen to it on

    some_payment_data = {
        "name": extension_builder_stub.name,
        "amount": payment.amount,
        "fee": payment.fee,
        "checking_id": payment.checking_id,
    }

    await websocket_updater(extension_builder_stub_id, str(some_payment_data))
