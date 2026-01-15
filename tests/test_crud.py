from uuid import uuid4

import pytest

from extension_builder_stub.crud import (  # type: ignore[import]
    create_owner_data,
    delete_owner_data,
    get_owner_data,
    get_owner_data_by_id,
    get_owner_data_ids_by_user,
    get_owner_data_paginated,
    update_owner_data,
)
from extension_builder_stub.models import (  # type: ignore[import]
    CreateOwnerData,
    OwnerData,
)


@pytest.mark.asyncio
async def test_create_and_get_owner_data():
    user_id = uuid4().hex

    data = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%> << cancel_comment >>"""
    )
    owner_data_one = await create_owner_data(user_id, data)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id

    owner_data_one = await get_owner_data(user_id, owner_data_one.id)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id
    """<< cancel_comment >>
    <% for field in owner_data.fields %>assert owner_data_one.<< field >> == data.<< field >>
    <% endfor%>  << cancel_comment >>"""

    data = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%> << cancel_comment >>"""
    )
    owner_data_two = await create_owner_data(user_id, data)
    assert owner_data_two.id is not None
    assert owner_data_two.user_id == user_id

    owner_data_list = await get_owner_data_ids_by_user(user_id=user_id)
    assert len(owner_data_list) == 2

    owner_data_page = await get_owner_data_paginated(user_id=user_id)
    assert owner_data_page.total == 2
    assert len(owner_data_page.data) == 2

    await delete_owner_data(user_id, owner_data_one.id)
    owner_data_list = await get_owner_data_ids_by_user(user_id=user_id)
    assert len(owner_data_list) == 1

    owner_data_page = await get_owner_data_paginated(user_id=user_id)
    assert owner_data_page.total == 1
    assert len(owner_data_page.data) == 1


@pytest.mark.asyncio
async def test_update_owner_data():
    user_id = uuid4().hex

    data = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%>  << cancel_comment >>"""
    )
    owner_data_one = await create_owner_data(user_id, data)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id

    owner_data_one = await get_owner_data(user_id, owner_data_one.id)
    assert owner_data_one.id is not None
    assert owner_data_one.user_id == user_id
    """<< cancel_comment >>
    <% for field in owner_data.fields %>assert owner_data_one.<< field >> == data.<< field >>
    <% endfor%>  << cancel_comment >>"""

    data_updated = CreateOwnerData(
        """<< cancel_comment >>
        <% for field in owner_data.random_fields_values %><< field >>
        <% endfor%>  << cancel_comment >>"""
    )
    owner_data_updated = OwnerData(**{**owner_data_one.dict(), **data_updated.dict()})

    await update_owner_data(owner_data_updated)
    owner_data_one = await get_owner_data_by_id(owner_data_one.id)
    """<< cancel_comment >>
    <% for field in owner_data.fields %>assert owner_data_one.<< field >> == owner_data_updated.<< field >>
    <% endfor%>  << cancel_comment >>"""
