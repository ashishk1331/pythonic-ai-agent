import requests as R
import json as J
import os as OS
import subprocess as SP
from urllib.parse import urlencode
from dotenv import load_dotenv
from utils import top_three

load_dotenv()

TINYFISH_HEADERS = {
    "X-API-Key": str(OS.getenv("TINYFISH_API_KEY")),
    "Content-Type": "application/json",
}


def web_search(query):
    print(f"[TOOL] [WEB_SEARCH] {query}")
    query = urlencode({"query": query})
    resp = R.get("https://api.search.tinyfish.ai?" + query, headers=TINYFISH_HEADERS)

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


def web_fetch(url):
    print(f"[TOOL] [WEB_FETCH] {url}")
    resp = R.post(
        "https://api.fetch.tinyfish.ai",
        headers=TINYFISH_HEADERS,
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


def run_command(command):
    print(f"[TOOL] [RUN_COMMAND] {command}")
    result = SP.run(command, shell=True, capture_output=True, text=True, timeout=30)

    if result.returncode != 0:
        print(
            f"[TOOL] [ERROR] Command failed with return code {result.returncode}: {result.stderr}"
        )
    else:
        print(f'[TOOL] [RESULT_RAN] "{command}" = \n{result.stdout}')
    return result.stdout or result.stderr


def read_file(path):
    print(f"[TOOL] [READ_FILE] {path}")
    with open(path, "r") as file:
        return file.read()


def write_file(path, content):
    print(f"[TOOL] [WRITE_FILE] {path} with content length {len(content)}")
    with open(path, "w") as file:
        file.write(content)
        return f"{path} written."


TOOLS_MAP = {
    "web_search": web_search,
    "web_fetch": web_fetch,
    "run_command": run_command,
    "read_file": read_file,
    "write_file": write_file,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web. Use this to find information or discover URLs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": "Fetch the full content of a URL as markdown. Use this when you already have a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch"}
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write contents to a file. It replaces the original content with new.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file."},
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]
