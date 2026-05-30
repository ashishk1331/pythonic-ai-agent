from dotenv import load_dotenv
load_dotenv()

from .llm import complete, context
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import choice

slash_commands = WordCompleter(['/exit', '/sessions'])

def bottom_toolbar():
    consumption = context.get_consumption()
    return HTML(
        f"{context.session_title} — " \
        f"Tokens Used: {consumption['current_tokens']} / {consumption['max_tokens_in_words']} — " \
        f"Context Used: ({consumption['percentage_used']}%) "
    )


def main():
    while True:
        message = prompt("> ", bottom_toolbar=bottom_toolbar, completer=slash_commands)
        if message.strip().lower() == "/exit":
            break
        if message.strip().lower() == "/sessions":
            available_sessions = context.get_available_sessions()

            if len(available_sessions) == 0:
                print("No available sessions found.")
                continue

            selected_session = choice(
                message="Available sessions:",
                options=[(session_id, title) for session_id, title in available_sessions] + [("exit", "Continue with current session")],
                default=available_sessions[0]
            )
            if selected_session[0] == "exit":
                print("Continuing with current session.")
                continue
            context.load_session(selected_session if isinstance(selected_session, str) else selected_session[0])
            continue
        if message.strip() == "":
            continue
        complete(message)


if __name__ == "__main__":
    main()
