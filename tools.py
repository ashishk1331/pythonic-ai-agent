import requests as R
import json as J
import subprocess as SP
from urllib.parse import urlencode
from utils import top_three
import constants as C
from docstring_parser import parse

TOOLS = []
TOOLS_MAP = {}


def tool(func):
    """ "A decorator to mark a function as a tool."""
    func.is_tool = True
    func.doc = parse(func.__doc__)
    TOOLS.append(
        {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.doc.short_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        param.arg_name: {
                            "type": "string",
                            "description": param.description,
                        }
                        for param in func.doc.params
                    },
                    "required": [param.arg_name for param in func.doc.params],
                },
            },
        }
    )
    TOOLS_MAP[func.__name__] = func

    def wrapper(*args, **kwargs):
        print(f"[TOOL] [{func.__name__}] {args} {kwargs}")
        return func(*args, **kwargs)

    return wrapper


@tool
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


@tool
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


@tool
def run_command(command):
    """Run a shell command and return its output.

    Args:
        command: The shell command to run.
    """
    result = SP.run(command, shell=True, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(
            f"[TOOL] [ERROR] Command failed with return code {result.returncode}: {result.stderr}"
        )
    else:
        print(f'[TOOL] [RESULT_RAN] "{command}" = \n{result.stdout}')
    return result.stdout or result.stderr


@tool
def read_file(path):
    """Read the contents of a file.

    Args:
        path: The path to the file.
    """
    with open(path, "r") as file:
        return file.read()


@tool
def write_file(path, content):
    """Write content to a file, replacing any existing content.

    Args:
        path: The path to the file.
        content: The content to write to the file.
    """
    with open(path, "w") as file:
        file.write(content)
        return f"{path} written."
