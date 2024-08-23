from flask import request
from app.character import character
from app.character.services import lists_service


@character.route('/create_list', methods=['POST'])
def create_list():
    data = request.json
    print(data)
    lists_service.create_list(name=data['listName'],
                              parent_list_id=data['parentListId'])
    return {'status': 'ok'}, 200
