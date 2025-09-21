from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from ui.review import ReviewUI
from datetime import datetime

class HomeUI(QWidget):
    def __init__(self, srs):
        super().__init__()
        self.srs = srs
        self.setWindowTitle("Flashcard App")
        self.resize(600, 500)

        # Background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#fdf6e3"))  # light beige
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.setup_stats()
        self.setup_due_cards()
        self.setup_review_buttons()

    def setup_stats(self):
        font_large = QFont("Segoe UI", 20, QFont.Bold)
        self.stats_label = QLabel()
        self.stats_label.setFont(font_large)
        self.stats_label.setStyleSheet("""
            background-color: #fff8f0;
            border-radius: 12px;
            padding: 20px;
            color: #333;
        """)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.stats_label)
        self.refresh_stats()

    def setup_due_cards(self):
        self.due_label = QLabel()
        self.due_label.setFont(QFont("Segoe UI", 16))
        self.due_label.setStyleSheet("""
            background-color: #fffdf5;
            border-radius: 12px;
            padding: 15px;
            color: #333;
        """)
        self.due_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.due_label)
        self.update_due_cards()

    def setup_review_buttons(self):
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        btn_style = """
        QPushButton {
            background-color: #ffffff;
            border: 2px solid #ccc;
            border-radius: 50px;
            padding: 20px;
            font-size: 16px;
        }
        QPushButton:hover { background-color: #f0f0f0; }
        QPushButton:pressed { background-color: #e0e0e0; }
        """

        self.random_btn = QPushButton("Random Speed Review")
        self.random_btn.setStyleSheet(btn_style)
        self.random_btn.clicked.connect(lambda: self.start_review(timed=True))
        self.button_layout.addWidget(self.random_btn)

        self.plain_btn = QPushButton("Plain Review")
        self.plain_btn.setStyleSheet(btn_style)
        self.plain_btn.clicked.connect(lambda: self.start_review(timed=False))
        self.button_layout.addWidget(self.plain_btn)

    def start_review(self, timed=False):
        due = self.srs.due_cards()
        max_cards = len(self.srs.deck)  # allow full deck review

        if not due:
            msg = "No cards are currently due for review.\nDo you want to review manually from the full deck?"
            manual = QMessageBox.question(
                self, "No cards due", msg,
                QMessageBox.Yes | QMessageBox.No
            )
            if manual == QMessageBox.No:
                return

        n, ok = QInputDialog.getInt(
            self, "Number of cards",
            f"Enter number of cards to review (max {max_cards}):",
            5, 1, max_cards
        )

        if ok and n > 0:
            review_window = ReviewUI(srs=self.srs, n_cards=n, home=self, timed=timed, allow_all=True)
            review_window.show()

    def update_due_cards(self):
        due_count = len(self.srs.due_cards())
        self.due_label.setText(f"{due_count} cards up for review")

    def refresh_stats(self):
        last_review = max((datetime.fromisoformat(d).date() for d in self.srs.stats_data.keys()), default=None)
        reviewed_this_month = self.srs.reviewed_this_month()
        avg_accuracy = self.srs.avg_accuracy_last_month()
        self.stats_label.setText(
            f"Last review: {last_review if last_review else 'N/A'}\n"
            f"Sentences reviewed this month: {reviewed_this_month}\n"
            f"Average accuracy last month: {avg_accuracy:.1f}%"
        )
