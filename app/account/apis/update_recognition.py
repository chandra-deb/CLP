from flask import request, jsonify
from flask_login import current_user
from fsrs import Card

from app import account, db
from app.models import UserRecognitionProgress


@account.route('/update_recognition', methods=['POST'])
def update_recognition():
    data = request.get_json()
    card = Card.from_dict(data)
    character_id = data.get('character_id')
    UserRecognitionProgress.update_recog_prog(card)
    user_progress = UserRecognitionProgress.query.filter_by(user_id=current_user.id, character_id=character_id).first()
    if user_progress:
        user_progress.update_recog_prog(card)
        db.session.commit()

    return jsonify({"message": "Rating updated successfully!"}), 200
