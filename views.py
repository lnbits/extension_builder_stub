# Description: Add your page endpoints here.

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer

from .crud import get_owner_data_by_id

extension_builder_stub_generic_router = APIRouter()


def extension_builder_stub_renderer():
    return template_renderer(["extension_builder_stub/templates"])


#######################################
##### ADD YOUR PAGE ENDPOINTS HERE ####
#######################################


# Backend admin page


@extension_builder_stub_generic_router.get("/", response_class=HTMLResponse)
async def index(req: Request, user: User = Depends(check_user_exists)):
    return extension_builder_stub_renderer().TemplateResponse(
        "extension_builder_stub/index.html", {"request": req, "user": user.json()}
    )


# Frontend shareable page


@extension_builder_stub_generic_router.get("/{owner_data_id}")
async def owner_data_public_page(req: Request, owner_data_id: str):
    owner_data = await get_owner_data_by_id(owner_data_id)
    if not owner_data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Owner Data does not exist.")

    return extension_builder_stub_renderer().TemplateResponse(
        "extension_builder_stub/public_page.html",
        {"request": req, "owner_data_id": owner_data_id},
    )
