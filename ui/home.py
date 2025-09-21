from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import datetime

class HomeUI(QWidget):
    def __init__(self, srs, stats):
        super().__init__()
        self.srs = srs
        self.stats = stats
        self.setWindowTitle("Flashcard Home")
        self.setFixedSize(600, 500)

        # Background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#fdf6e3"))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        # Stats
        self.stats_label = QLabel(self.get_stats_text())
        self.stats_label.setFont(QFont("Segoe UI", 16))
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)

        # Cards due
        self.due_label = QLabel(f"{len(self.srs.get_due_cards())}\nCards up for review")
        self.due_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.due_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.due_label)

        # Buttons
        speed_btn = QPushButton("Random Speed Review")
        plain_btn = QPushButton("Plain Review")
        for b in (speed_btn, plain_btn):
            b.setFont(QFont("Segoe UI", 14))
            layout.addWidget(b)
        speed_btn.clicked.connect(lambda: self.start_review(timed=True))
        plain_btn.clicked.connect(lambda: self.start_review(timed=False))

    def get_stats_text(self):
        last = self.stats.last_review or "N/A"
        return (f"Last review: {last}\n"
                f"Sentences reviewed this month: {self.stats.reviewed_this_month}\n"
                f"Avg accuracy last month: {self.stats.avg_accuracy_last_month}%")

    def start_review(self, timed):
        num, ok = QInputDialog.getInt(self, "Select number", "How many cards to review?",
                                      5, 1, len(self.srs.get_due_cards()))
        if ok:
            from ui.review import ReviewUI
            self.review_window = ReviewUI(self.srs, num_cards=num, timed=timed)
            self.review_window.show()
            self.close()
