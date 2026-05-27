import requests as R
import json as J
import os as OS
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

TINYFISH_HEADERS = {
    'X-API-Key': str(OS.getenv('TINYFISH_API_KEY')),
    'Content-Type': 'application/json',
}

def web_search(query):
    print(f'[TOOL] [WEB_SEARCH] {query}')
    query = urlencode({'query': query})
    resp = R.get(
        'https://api.search.tinyfish.ai?' + query, 
        headers=TINYFISH_HEADERS
    )
    data = resp.json()
    return data['results']

def web_fetch(url):
    print(f'[TOOL] [WEB_FETCH] {url}')
    resp = R.post(
        'https://api.fetch.tinyfish.ai',
        headers=TINYFISH_HEADERS,
        json={
            'urls': [url],
            'format': 'markdown',
        },
    )
    data = resp.json()
    return data['results'][0]


def echo(text):
    print(f'[TOOL] [ECHO] {text}')
    return f'Echoed: {text}'

TOOLS_MAP = {
    "echo": echo,
    "web_search": web_search,
    "web_fetch": web_fetch,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "echo",
            "description": "Echo the input text. After use, say 'Echoed'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to echo"
                    }
                },
                "required": ["text"]
            }
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
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
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
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch"
                    }
                },
                "required": ["url"]
            }
        },
    },
]

# print(J.dumps(web_search("supermemory blog"), indent=2))
# print(J.dumps(web_fetch("https://supermemory.ai/blog/building-code-chunk-ast-aware-code-chunking/"), indent=2))