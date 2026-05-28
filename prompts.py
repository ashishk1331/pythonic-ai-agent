def get_system_prompt():
    with open("./prompts/system.md", "r") as file:
        return file.read()
    return "You are a helpful assistant who always speak briefly."


def get_compaction_prompt():
    with open("./prompts/compaction.md", "r") as file:
        return file.read()
    return "Please summarize the following conversation:"
