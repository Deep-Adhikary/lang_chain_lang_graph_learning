import json
from dataclasses import dataclass

from langchain.tools import tool


@dataclass
class DogInfo:
    name: str
    description: str

@tool
def get_dog_info(dog_name: str) -> str:
    """Dog info tool that returns information about a dog breed."""
    with open("tools/data.json", "r", encoding="utf-8") as f:
        dog_data = json.load(f)

    dog_data = {
        item["attributes"]["name"]: item["attributes"]["description"]
        for item in dog_data["data"]
        if item["attributes"]["name"].lower().strip() == dog_name.lower().strip()
    }
    return dog_data.get(dog_name, "Information not found for this dog breed.")
