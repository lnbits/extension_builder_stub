from uuid import uuid4

import pytest

from extension_builder_stub.crud import (  # type: ignore[import]
    create_owner_data,
    get_owner_data_ids_by_user,
)
from extension_builder_stub.models import (  # type: ignore[import]
    CreateOwnerData,
)


@pytest.mark.asyncio
async def test_create_owner_data():
    user_id = uuid4().hex

    data = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%>
        << cancel_comment >>"""
    )
    owner_data_one = await create_owner_data(user_id, data)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id

    data = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%>
        << cancel_comment >>"""
    )
    owner_data_two = await create_owner_data(user_id, data)
    assert owner_data_two.id is not None
    assert owner_data_two.user_id == user_id

    rooms = await get_owner_data_ids_by_user(user_id=user_id)
    assert len(rooms) == 2
