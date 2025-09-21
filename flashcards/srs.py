from datetime import date, timedelta, datetime
import random
import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

class FlashcardSRS:
    def __init__(self, deck):
        self.deck = deck
        self.cards_file = DATA_DIR / "srs_cards.json"
        self.stats_file = DATA_DIR / "monthly_stats.json"
        self.accuracy_file = DATA_DIR / "accuracy.json"

        # Load persistent data
        self.cards_data = self._load(self.cards_file)
        self.stats_data = self._load(self.stats_file)
        self.accuracy_data = self._load(self.accuracy_file)

        self._prune_old_stats()

        # Initialize deck cards with persisted data
        for card in self.deck:
            info = self.cards_data.get(card.card_id, {})
            card.interval = info.get("interval", 0)
            card.due_date = datetime.fromisoformat(info["due_date"]).date() if "due_date" in info else None
            card.easiness = info.get("easiness", 2.5)

    def _load(self, path):
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save(self, path, data):
        path.write_text(json.dumps(data, indent=2))

    def _prune_old_stats(self):
        today = date.today()
        cutoff = today - timedelta(days=30)
        # Stats pruning
        self.stats_data = {d:v for d,v in self.stats_data.items() if datetime.fromisoformat(d).date() >= cutoff}
        self.accuracy_data = {d:v for d,v in self.accuracy_data.items() if datetime.fromisoformat(d).date() >= cutoff}
        self._save(self.stats_file, self.stats_data)
        self._save(self.accuracy_file, self.accuracy_data)

    def due_cards(self):
        today = date.today()
        return [card for card in self.deck if not card.due_date or card.due_date <= today]

    def mark_reviewed(self, card, correct: bool):
        today = date.today().isoformat()
        # SM-2 style: simple interval & easiness adjustment
        if correct:
            card.interval = card.interval*2 if card.interval else 1
            card.easiness = max(1.3, card.easiness + 0.1)
        else:
            card.interval = 1
            card.easiness = max(1.3, card.easiness - 0.2)
        card.due_date = date.today() + timedelta(days=card.interval)

        # Save per-card info
        self.cards_data[card.card_id] = {
            "interval": card.interval,
            "due_date": card.due_date.isoformat(),
            "easiness": card.easiness
        }
        self._save(self.cards_file, self.cards_data)

        # Update stats
        self.stats_data[today] = self.stats_data.get(today, 0) + 1
        self._save(self.stats_file, self.stats_data)

        # Update accuracy
        acc = self.accuracy_data.get(today, {"correct":0, "total":0})
        acc["total"] += 1
        if correct:
            acc["correct"] += 1
        self.accuracy_data[today] = acc
        self._save(self.accuracy_file, self.accuracy_data)

    def random_review(self, n=None):
        due = self.due_cards()
        random.shuffle(due)
        return due[:n] if n else due

    # New helper methods for HomeUI stats
    def reviewed_this_month(self):
        return sum(self.stats_data.values())

    def avg_accuracy_last_month(self):
        if not self.accuracy_data:
            return 0.0
        valid_days = [v for v in self.accuracy_data.values() if v["total"]>0]
        if not valid_days:
            return 0.0
        return round(sum(v["correct"]/v["total"]*100 for v in valid_days)/len(valid_days),1)
