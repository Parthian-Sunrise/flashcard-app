from dataclasses import dataclass
from typing import List, Optional
from datetime import date
import hashlib

@dataclass
class Flashcard:
    def __init__(self, question, answer, choices):
        self.question = question
        self.answer = answer
        self.choices = choices
        self.interval = 0
        self.due_date = None
        self.easiness = 2.5

        # Unique ID for SRS persistence
        self.card_id = hashlib.md5(question.encode("utf-8")).hexdigest()


@dataclass
class ReviewStats:
    last_review: Optional[date]
    reviewed_this_month: int
    avg_accuracy_last_month: float
