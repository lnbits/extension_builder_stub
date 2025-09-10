from lnbits.core.models import Payment
from lnbits.core.services import create_invoice
from loguru import logger

from .crud import (
    create_client_data,
    create_extension_settings,
    get_client_data_by_id,
    get_extension_settings,
    get_owner_data_by_id,
    update_client_data,
    update_extension_settings,
)
from .models import (
    ClientDataPaymentRequest,
    CreateClientData,
    ExtensionSettings,
)


async def payment_request_for_client_data(
    owner_data_id: str,
    data: CreateClientData,
) -> ClientDataPaymentRequest:

    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise ValueError("Invalid owner data ID.")

    client_data = await create_client_data(owner_data_id, data)

    payment: Payment = await create_invoice(
        wallet_id=owner_data.wallet_id,  # todo
        amount=client_data.amount_sats,  # todo
        extra={"tag": "extension_builder_stub", "client_data_id": client_data.id},
        memo=f"Payment for {owner_data.name}. " f"Client Data ID: {client_data.id}",
    )
    return ClientDataPaymentRequest(
        client_data_id=client_data.id,
        payment_hash=payment.payment_hash,
        payment_request=payment.bolt11,
    )


async def payment_received_for_client_data(payment: Payment) -> bool:
    client_data_id = payment.extra.get("client_data_id")
    if not client_data_id:
        logger.warning("Payment does not have a client_data_id in extra.")
        return False

    client_data = await get_client_data_by_id(client_data_id)
    if not client_data:
        logger.warning(f"No client data found for ID: {client_data_id}")
        return False

    client_data.paid = True  # type: ignore
    await update_client_data(client_data)
    logger.info(f"Client data {client_data_id} marked as paid.")
    return True


#  <% if settings_table.has_settings %> << cancel_comment >>
async def get_settings(user_id: str) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    return settings


async def update_settings(user_id: str, data: ExtensionSettings) -> ExtensionSettings:
    settings = await get_extension_settings(user_id)
    if not settings:
        settings = await create_extension_settings(user_id, ExtensionSettings())
    await update_extension_settings(user_id, data)

    return settings


# <% endif %> << cancel_comment >>
