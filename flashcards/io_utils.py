import json
from .models import Flashcard

def load_flashcards(path="data/flashcards.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return [Flashcard(**card) for card in data]