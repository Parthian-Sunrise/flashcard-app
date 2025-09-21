import sys
from PyQt5.QtWidgets import QApplication
from flashcards.io_utils import load_flashcards
from flashcards.models import ReviewStats
from flashcards.srs import FlashcardSRS
from ui.home import HomeUI
from datetime import date

deck = load_flashcards()
srs = FlashcardSRS(deck)
stats = ReviewStats(last_review=date.today(), reviewed_this_month=12, avg_accuracy_last_month=87.5)

app = QApplication(sys.argv)
home = HomeUI(srs)
home.show()
sys.exit(app.exec_())
