from datetime import datetime, timezone

from fsrs import FSRS, Card, Rating

f = FSRS()

card = Card()
rating = Rating.Good
card, review_log = f.review_card(card, rating)
# def print_data()
print('Scheduled Days:', review_log.scheduled_days)
print('Last Review', card.last_review)
print('Difficulty:', card.difficulty)
print('Stability:', card.stability)
print('Retriveablity:', card.get_retrievability(now=datetime.now(tz=timezone.utc)))
print(card.reps)

rating = rating.Good
card = Card.from_dict(card.to_dict())
card, review_log = f.review_card(card, rating)
print(card.reps)

print('Scheduled Days:', review_log.scheduled_days)
print('Last Review', card.last_review)
print('Difficulty:', card.difficulty)
print('Stability:', card.stability)
print('Retriveablity:', card.get_retrievability(now=datetime.now(tz=timezone.utc)))
print(card.reps)

rating = rating.Hard
card = Card.from_dict(card.to_dict())
card, review_log = f.review_card(card, rating)
print(card.reps)

print('Scheduled Days:', review_log.scheduled_days)
print('Last Review', card.last_review)
print('Difficulty:', card.difficulty)
print('Stability:', card.stability)
print('Retriveablity:', card.get_retrievability(now=datetime.now(tz=timezone.utc)))

rating = rating.Hard
card = Card.from_dict(card.to_dict())
card, review_log = f.review_card(card, rating)
print(card.reps)

print('Scheduled Days:', review_log.scheduled_days)
print('Last Review', card.last_review)
print('Difficulty:', card.difficulty)
print('Stability:', card.stability)
print('Retriveablity:', card.get_retrievability(now=datetime.now(tz=timezone.utc)))

scheduling_cards = f.repeat(card, datetime.now(tz=timezone.utc))
print(scheduling_cards[rating].card.to_dict())
