from llm import complete, context
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML


def bottom_toolbar():
    consumption = context.get_consumption()
    return HTML(
        f"Tokens Used: {consumption['current_tokens']} / {consumption['max_tokens_in_words']} Context Used: ({consumption['percentage_used']}%)"
    )


def main():
    while True:
        message = prompt("> ", bottom_toolbar=bottom_toolbar)
        if message.strip().lower() == "exit":
            break
        if message.strip() == "":
            continue
        complete(message)


if __name__ == "__main__":
    main()
