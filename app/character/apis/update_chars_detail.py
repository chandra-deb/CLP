from flask import request
from app.character import character
from app.character.services import lists_service


@character.route('/update_chars_detail', methods=['POST'])
def update_chars_detail():
    data = request.json
    print(data)

    print(type(data))
    lists_service.update_memory_strength(data)
    return {'status': 'ok'}