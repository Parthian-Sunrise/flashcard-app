from dataclasses import dataclass, field
import datetime

@dataclass
class Flashcard:
    question: str
    answer: str
    choices: list
    last_review: datetime.date = field(default=None)
    next_review: datetime.date = field(default=None)
    interval: int = 1
    ease: float = 2.5
    repetitions: int = 0

@dataclass
class ReviewStats:
    last_review: datetime.date = None
    reviewed_this_month: int = 0
    avg_accuracy_last_month: float = 0.0
