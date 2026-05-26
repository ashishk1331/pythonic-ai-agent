import os as OS
import json as J
import requests as R
from tools import TOOLS_MAP, tools
from dotenv import load_dotenv

load_dotenv()

headers = {
    'Authorization': f'Bearer {OS.getenv("OPENROUTER_API_KEY")}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'baidu/cobuddy:free',
    'max_tokens': 1_000,
    'temperature': 0.7
}

context = [
    {'role': 'system', 'content': 'You are a helpful assistant who always speak briefly.'},
]

def complete(message, max_tool_calls=5):

    if max_tool_calls <= 0:
        print('[ERROR] Maximum tool call limit reached.')
        return

    if message is not None:
        context.append({ 'role': 'user', 'content': message })

    resp = R.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=payload | { 'messages': context, 'tools': tools },
    )

    if resp.status_code != 200:
        print(f'[ERROR] API request failed with status code {resp.status_code}: {resp.text}')
        return

    data = resp.json()
    message = data['choices'][0]['message']

    if message.get('tool_calls'):
        context.append(message)
        for tool_call in message['tool_calls']:
            name = tool_call['function']['name']
            args = J.loads(tool_call['function']['arguments'])

            result = TOOLS_MAP[name](**args)

            context.append({
                'role': 'tool',
                'tool_call_id': tool_call['id'],
                'content': str(result),
            })
        complete(None, max_tool_calls - 1)
    else:
        context.append({ 'role': 'assistant', 'content': message['content'] })
        print(f'< {message["content"]}\n')


def stream(message):
    context.append({ 'role': 'user', 'content': message })

    resp = R.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        json=payload | { 'messages': context, 'stream': True },
        stream=True,
    )

    print('< ', end='')
    for line in resp.iter_lines():
        if not line:
            continue
        line = line.decode('utf-8')
        if line.startswith(':'):
            continue
        line = line[6:]
        if line == '[DONE]':
            break
        print(J.loads(line)['choices'][0]['delta']['content'], end='', flush=True)
    print()

def debug_context():
    print(f'---\n[CONTEXT STARTS]\n\n{J.dumps(context, indent=2)}\n\n[CONTEXT ENDS]\n---')