def SystemMessage(content: str):
    return { "role": "system", "content": content }

def UserMessage(message: str):
    return { "role": "user", "content": message }