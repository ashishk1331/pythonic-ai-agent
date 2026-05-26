def echo(text):
    print(f'[TOOL] [ECHO] {text}')
    return f'Echoed: {text}'

TOOLS_MAP = {
    "echo": echo,
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
]