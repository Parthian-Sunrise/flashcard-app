import datetime

class FlashcardSRS:
    def __init__(self, deck):
        self.deck = deck
        self.today = datetime.date.today()

    def get_due_cards(self):
        return [c for c in self.deck if not c.next_review or c.next_review <= self.today]

    def update_card(self, card, correct):
        if card.repetitions is None:
            card.repetitions = 0
            card.interval = 1
            card.ease = 2.5
        if correct:
            card.repetitions += 1
            card.interval = max(1, round(card.interval * card.ease))
        else:
            card.repetitions = 0
            card.interval = 1
        card.next_review = self.today + datetime.timedelta(days=card.interval)
        card.last_review = self.today
