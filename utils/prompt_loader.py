"""
Utility to load prompt templates from the prompts folder.
"""

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load a prompt from the prompts directory.

    Example:
        load_prompt("shipment.txt")
    """

    prompt_path = PROMPTS_DIR / filename

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file '{filename}' not found."
        )

    with open(prompt_path, "r", encoding="utf-8") as file:
        return file.read()