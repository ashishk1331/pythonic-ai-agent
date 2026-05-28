from tools.registry import register_tool
from urllib.parse import urlencode
import requests as R
import constants as C
from utils import top_three

@register_tool
def web_search(query):
    """Search the web. Use this to find information or discover URLs.

    Args:
        query: The search query.
    """
    query = urlencode({"query": query})
    resp = R.get(f"{C.TINYFISH_SEARCH_URL}?{query}", headers=C.TINYFISH_HEADERS)

    if resp.status_code != 200:
        print(
            f"[TOOL] [ERROR] Search failed with status code {resp.status_code}: {resp.text}"
        )
        return f"Failed to search for {query}"

    data = resp.json()
    print(
        f'[TOOL] [WEB_SEARCH_RESULT] "{query}" = {", ".join(top_three([result["site_name"].lstrip("www.") for result in data["results"]]))}'
    )
    return data["results"]


@register_tool
def web_fetch(url):
    """Fetch the full content of a URL as markdown. Use this when you already have a URL.

    Args:
        url: The URL to fetch.
    """
    resp = R.post(
        C.TINYFISH_FETCH_URL,
        headers=C.TINYFISH_HEADERS,
        json={
            "urls": [url],
            "format": "markdown",
        },
    )

    if resp.status_code != 200:
        print(
            f"[TOOL] [ERROR] Fetch failed with status code {resp.status_code}: {resp.text}"
        )
        return f"Failed to fetch {url}"

    data = resp.json()
    print(f"[TOOL] [WEB_FETCH_RESULT] {url} = {data['results'][0]['description']}")
    return data["results"][0]