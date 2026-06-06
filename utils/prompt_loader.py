from pathlib import Path


def load_prompt(file_name: str) -> str:

    prompt_path = (
        Path(__file__).parent.parent
        / "prompts"
        / file_name
    )

    with open(prompt_path, "r") as file:
        return file.read()