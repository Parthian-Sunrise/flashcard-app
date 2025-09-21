import sys
import random
from PyQt5.QtWidgets import QApplication
from flashcards.io_utils import load_flashcards
from flashcards.models import ReviewStats
from flashcards.srs import FlashcardSRS
from ui.home import HomeUI

# Optional: You can also import ReviewUI if needed for standalone testing
# from ui.review import ReviewUI

def main():
    # Load flashcards
    deck = load_flashcards()

    # Initialize SRS system
    srs = FlashcardSRS(deck)

    # Load stats (you can implement persistent storage later)
    stats = ReviewStats(
        last_review=None,
        reviewed_this_month=0,
        avg_accuracy_last_month=0.0
    )

    # Launch app
    app = QApplication(sys.argv)
    home_window = HomeUI(srs, stats)
    home_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
