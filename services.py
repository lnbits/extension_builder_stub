from lnbits.core.models import Payment
from lnbits.core.services import create_invoice

from .crud import (
    create_client_data,
    create_extension_settings,
    get_extension_settings,
    get_owner_data_by_id,
    update_extension_settings,
)
from .models import (
    ClientDataPaymentRequest,
    CreateClientData,
    ExtensionSettings,
)


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
        extra={"tag": "extension_builder_stub"},
        memo=f"Payment for {owner_data.name}.",  # todo
    )
    return ClientDataPaymentRequest(
        client_data_id=client_data.id,
        payment_hash=payment.payment_hash,
        payment_request=payment.bolt11,
    )


# <% endif %> << cancel_comment >>
