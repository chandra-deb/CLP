from flask import request
from app.character import character
from app.character.services import lists_service


@character.route('/pin_list', methods=['POST'])
def pin_list():
    data = request.json
    print(data)
    list_id = data['listId']
    lists_service.pin_list(list_id=list_id)
    return {'status': 'ok'}, 200
