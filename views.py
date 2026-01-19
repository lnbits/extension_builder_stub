# Description: Add your page endpoints here.


from fastapi import APIRouter, Depends
from lnbits.core.views.generic import index, index_public
from lnbits.decorators import check_account_exists
from lnbits.helpers import template_renderer

extension_builder_stub_generic_router = APIRouter()


def extension_builder_stub_renderer():
    return template_renderer(["extension_builder_stub/templates"])


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page
extension_builder_stub_generic_router.add_api_route(
    "/", methods=["GET"], endpoint=index, dependencies=[Depends(check_account_exists)]
)


# Frontend shareable page


# <% if public_page.has_public_page %> << cancel_comment >>
extension_builder_stub_generic_router.add_api_route("/{owner_data_id}", methods=["GET"], endpoint=index_public)


# <% endif %> << cancel_comment >>
