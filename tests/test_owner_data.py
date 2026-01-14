import pytest
from extension_builder_stub.crud import (  # type: ignore[import]
    create_owner_data,
    get_auction_room,
    update_auction_room,
)
from extension_builder_stub.models import (  # type: ignore[import]
    OwnerData,
    CreateOwnerData,
    AuctionRoomConfig,
    EditAuctionRoomData,
)
from extension_builder_stub.services import get_user_auction_rooms  # type: ignore[import]
from lnbits.helpers import urlsafe_short_hash


@pytest.mark.asyncio
async def test_create_owner_data():
    user_id = "9e95a704fbc047d79edff94a1cdda70c"

    owner_data = CreateOwnerData(
        id=urlsafe_short_hash(),
        user_id=user_id,
        name="room one",
        fee_wallet_id="w123",
        currency="USD",
        type="auction",
        description="test 1 description",
        extra=AuctionRoomConfig(),
    )
    owner_data_one = await create_owner_data(owner_data)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id
    assert owner_data_one.fee_wallet_id == "w123"

    owner_data = OwnerData(
        id=urlsafe_short_hash(),
        user_id=user_id,
        fee_wallet_id="w123",
        currency="USD",
        type="fixed_price",
        name="room two",
        description="test 2 description",
        extra=AuctionRoomConfig(),
    )

    owner_data_two = await create_owner_data(owner_data)
    assert owner_data_two.id is not None
    assert owner_data_two.user_id == user_id
    assert owner_data_two.fee_wallet_id == "w123"
    assert owner_data_two.type == "fixed_price"

    rooms = await get_user_auction_rooms(user_id=user_id)
    assert len(rooms) == 2
