class Stats:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / "stats.json"

        if self.stats_file.exists():
            with open(self.stats_file) as f:
                data = json.load(f)
        else:
            data = {}

        self.last_review = date.fromisoformat(data.get("last_review")) if data.get("last_review") else None
        self.reviewed_this_month = data.get("reviewed_this_month", 0)
        self.correct_this_month = data.get("correct_this_month", 0)

    def mark_review(self, correct: bool):
        today = date.today()
        self.last_review = today
        self.reviewed_this_month += 1
        if correct:
            self.correct_this_month += 1
        self.save()

    @property
    def avg_accuracy_last_month(self):
        # For simplicity: assume last month = same as this month for now
        if self.reviewed_this_month == 0:
            return 0.0
        return (self.correct_this_month / self.reviewed_this_month) * 100

    def save(self):
        data = {
            "last_review": self.last_review.isoformat() if self.last_review else None,
            "reviewed_this_month": self.reviewed_this_month,
            "correct_this_month": self.correct_this_month
        }
        with open(self.stats_file, "w") as f:
            json.dump(data, f, indent=2)
