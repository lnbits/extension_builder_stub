# Description: A place for helper functions.

from fastapi import Request
from lnurl.core import encode as lnurl_encode


def lnurler(myex_id: str, route_name: str, req: Request) -> str:
    url = req.url_for(route_name, extension_builder_stub_id=myex_id)
    url_str = str(url)
    if url.netloc.endswith(".onion"):
        url_str = url_str.replace("https://", "http://")
    return str(lnurl_encode(url_str))
