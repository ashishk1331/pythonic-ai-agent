from docstring_parser import parse

TOOLS = []
TOOLS_MAP = {}


def register_tool(func):
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
