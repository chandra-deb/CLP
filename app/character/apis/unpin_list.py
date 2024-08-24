from flask import request
from app.character import character
from app.character.services import lists_service


@character.route('/unpin_list', methods=['POST'])
def unpin_list():
    data = request.json
    print(data)
    list_id = data['listId']
    lists_service.unpin_list(list_id=list_id)
    return {'status': 'ok'}, 200
