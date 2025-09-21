def run_quiz(deck):
    score = 0
    for i, card in enumerate(deck, 1):
        correct = ask_question(card)
        if correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. Answer: {card.answer}")
    print(f"\nFinal Score: {score}/{len(deck)}")