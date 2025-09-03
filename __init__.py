import asyncio

from fastapi import APIRouter
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .crud import db
from .tasks import wait_for_paid_invoices
from .views import extension_builder_stub_generic_router
from .views_api import extension_builder_stub_api_router

extension_builder_stub_ext: APIRouter = APIRouter(
    prefix="/extension_builder_stub", tags=["extension_builder_stub_name"]
)
extension_builder_stub_ext.include_router(extension_builder_stub_generic_router)
extension_builder_stub_ext.include_router(extension_builder_stub_api_router)


extension_builder_stub_static_files = [
    {
        "path": "/extension_builder_stub/static",
        "name": "extension_builder_stub_static",
    }
]

scheduled_tasks: list[asyncio.Task] = []


def extension_builder_stub_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def extension_builder_stub_start():
    task = create_permanent_unique_task(
        "ext_extension_builder_stub", wait_for_paid_invoices
    )
    scheduled_tasks.append(task)


__all__ = [
    "db",
    "extension_builder_stub_ext",
    "extension_builder_stub_static_files",
    "extension_builder_stub_start",
    "extension_builder_stub_stop",
]