# Description: Add your page endpoints here.

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from lnbits.core.models import User
from lnbits.decorators import check_user_exists
from lnbits.helpers import template_renderer
from lnbits.settings import settings

from .crud import get_extension_builder_stub
from .helpers import lnurler

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


@extension_builder_stub_generic_router.get("/{extension_builder_stub_id}")
async def extension_builder_stub(req: Request, extension_builder_stub_id):
    myex = await get_extension_builder_stub(extension_builder_stub_id)
    if not myex:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )
    return extension_builder_stub_renderer().TemplateResponse(
        "extension_builder_stub/extension_builder_stub.html",
        {
            "request": req,
            "extension_builder_stub_id": extension_builder_stub_id,
            "lnurlpay": lnurler(myex.id, "extension_builder_stub.api_lnurl_pay", req),
            "web_manifest": f"/extension_builder_stub/manifest/{extension_builder_stub_id}.webmanifest",
        },
    )


# Manifest for public page, customise or remove manifest completely


@extension_builder_stub_generic_router.get("/manifest/{extension_builder_stub_id}.webmanifest")
async def manifest(extension_builder_stub_id: str):
    extension_builder_stub = await get_extension_builder_stub(extension_builder_stub_id)
    if not extension_builder_stub:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="MyExtension does not exist."
        )

    return {
        "short_name": settings.lnbits_site_title,
        "name": extension_builder_stub.name + " - " + settings.lnbits_site_title,
        "icons": [
            {
                "src": (
                    settings.lnbits_custom_logo
                    if settings.lnbits_custom_logo
                    else "https://cdn.jsdelivr.net/gh/lnbits/lnbits@0.3.0/docs/logos/lnbits.png"
                ),
                "type": "image/png",
                "sizes": "900x900",
            }
        ],
        "start_url": "/extension_builder_stub/" + extension_builder_stub_id,
        "background_color": "#1F2234",
        "description": "Minimal extension to build on",
        "display": "standalone",
        "scope": "/extension_builder_stub/" + extension_builder_stub_id,
        "theme_color": "#1F2234",
        "shortcuts": [
            {
                "name": extension_builder_stub.name + " - " + settings.lnbits_site_title,
                "short_name": extension_builder_stub.name,
                "description": extension_builder_stub.name + " - " + settings.lnbits_site_title,
                "url": "/extension_builder_stub/" + extension_builder_stub_id,
            }
        ],
    }
