from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import random
from flashcards.quiz_logic import check_answer
import simpleaudio as sa

class ReviewUI(QWidget):
    def __init__(self, srs, num_cards, timed=False):
        super().__init__()
        self.srs = srs
        self.num_cards = num_cards
        self.timed = timed
        self.deck = random.sample(srs.get_due_cards(), num_cards)
        self.current = 0
        self.current_choices = []

        self.setWindowTitle("Review Session")
        self.setFixedSize(600, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Question
        self.question_label = QLabel("")
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(self.question_label)

        # Buttons
        self.choice_buttons = []
        for i in range(4):
            btn = QPushButton("")
            btn.setStyleSheet("""
                QPushButton {background-color: #ffffff; border-radius: 12px; padding: 10px;}
                QPushButton:pressed {background-color: #e0e0e0;}
            """)
            btn.clicked.connect(lambda checked, idx=i: self.check(idx))
            layout.addWidget(btn)
            self.choice_buttons.append(btn)

        # Timer bar
        if timed:
            self.progress = QProgressBar()
            self.progress.setMaximum(5000)
            layout.addWidget(self.progress)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_timer)
            self.time_remaining = 5000

        self.show_card()

    def play_sound(self, filename):
        try:
            sa.WaveObject.from_wave_file(filename).play()
        except:
            pass

    def show_card(self):
        if self.current >= len(self.deck):
            QMessageBox.information(self, "Session Finished", "Review session completed!")
            self.close()
            return

        card = self.deck[self.current]
        self.question_label.setText(card.question)
        choices = card.choices[:]
        random.shuffle(choices)
        self.current_choices = choices

        for btn, choice in zip(self.choice_buttons, choices):
            btn.setText(choice)
            btn.setEnabled(True)
            btn.setStyleSheet("""
                QPushButton {background-color: #ffffff; border-radius: 12px; padding: 10px;}
                QPushButton:pressed {background-color: #e0e0e0;}
            """)

        if self.timed:
            self.time_remaining = 5000
            self.progress.setValue(self.time_remaining)
            self.timer.start(50)

    def update_timer(self):
        self.time_remaining -= 50
        self.progress.setValue(self.time_remaining)
        if self.time_remaining <= 0:
            self.timer.stop()
            self.check(-1)  # time ran out, mark as wrong

    def check(self, idx):
        card = self.deck[self.current]
        correct = (idx != -1 and self.current_choices[idx] == card.answer)
        if correct:
            self.play_sound("sounds/correct.wav")
        else:
            self.play_sound("sounds/wrong.wav")
        self.srs.update_card(card, correct)

        for btn in self.choice_buttons:
            btn.setEnabled(False)
        if self.timed:
            self.timer.stop()

        self.current += 1
        QTimer.singleShot(500, self.show_card)
