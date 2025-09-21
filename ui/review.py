from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import random
import simpleaudio as sa
from flashcards.quiz_logic import check_answer

class ReviewUI(QWidget):
    def __init__(self, srs, n_cards, timed=False, home=None, allow_all=False):
        super().__init__()
        self.srs = srs
        self.timed = timed
        self.home = home
        self.allow_all = allow_all
        if allow_all:
            self.deck = random.sample(srs.deck, min(n_cards, len(srs.deck)))
        else:
            self.deck = srs.random_review(n_cards)
        self.current = 0
        self.current_choices = []

        self.setWindowTitle("Flashcard Review")
        self.resize(500, 400)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#fdf6e3"))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # Question label
        self.question_label = QLabel("")
        self.question_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            background-color: #fffdf5;
            border-radius: 12px;
            padding: 20px;
            color: #333;
        """)
        self.layout.addWidget(self.question_label)

        # Timer bar
        if self.timed:
            self.progress_bar = QProgressBar()
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(100)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #ccc; border-radius: 8px; background-color: #f0f0f0; }
                QProgressBar::chunk { background-color: #4caf50; border-radius: 8px; }
            """)
            self.layout.addWidget(self.progress_bar)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_timer)
            self.time_left = 5000  # 5s

        # Choice buttons
        self.choice_buttons = []
        for i in range(4):
            btn = QPushButton("")
            btn.setFont(QFont("Segoe UI", 14))
            btn.setStyleSheet("""
                QPushButton { background-color: #ffffff; border: 2px solid #ccc; border-radius: 12px; padding: 12px; color: #333; }
                QPushButton:hover { background-color: #f0f0f0; }
                QPushButton:pressed { background-color: #e0e0e0; }
            """)
            btn.clicked.connect(lambda checked, idx=i: self.check(idx))
            self.layout.addWidget(btn)
            self.choice_buttons.append(btn)

        self.show_card()

    def play_sound(self, filename):
        try:
            wave_obj = sa.WaveObject.from_wave_file(filename)
            wave_obj.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def show_card(self):
        if self.current < len(self.deck):
            card = self.deck[self.current]
            self.question_label.setText(card.question)
            choices = card.choices[:]
            random.shuffle(choices)
            self.current_choices = choices

            for btn, choice in zip(self.choice_buttons, choices):
                btn.setText(choice)
                btn.setEnabled(True)
                btn.setStyleSheet("""
                    QPushButton { background-color: #ffffff; border: 2px solid #ccc; border-radius: 12px; padding: 12px; color: #333; }
                    QPushButton:hover { background-color: #f0f0f0; }
                    QPushButton:pressed { background-color: #e0e0e0; }
                """)

            if self.timed:
                self.time_left = 5000
                self.progress_bar.setValue(100)
                self.timer.start(50)
        else:
            self.finish_review()
            QMessageBox.information(self, "Done", "Review finished!")

    def update_timer(self):
        self.time_left -= 50
        self.progress_bar.setValue(int(self.time_left / 50 / 100 * 100))
        if self.time_left <= 0:
            self.timer.stop()
            self.next_card()

    def check(self, idx):
        card = self.deck[self.current]
        choice = self.current_choices[idx]
        btn = self.choice_buttons[idx]

        correct = check_answer(card, choice)
        self.srs.mark_reviewed(card, correct)

        if self.home:
            self.home.refresh_stats()
            self.home.update_due_cards()

        if correct:
            btn.setStyleSheet("background-color: #a8e6a2; border-radius: 12px;")
            self.play_sound("sounds/correct.wav")
        else:
            btn.setStyleSheet("background-color: #f7a6a6; border-radius: 12px;")
            self.play_sound("sounds/wrong.wav")
            QMessageBox.warning(self, "Result", f"❌ Wrong. Answer: {card.answer}")

        for b in self.choice_buttons:
            b.setEnabled(False)

        if self.timed:
            self.timer.stop()
        QTimer.singleShot(1000, self.next_card)

    def next_card(self):
        self.current += 1
        self.show_card()

    def finish_review(self):
        if self.home:
            self.home.update_due_cards()
            self.home.refresh_stats()
        self.close()
