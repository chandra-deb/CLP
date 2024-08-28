from flask import request
from app.character import character
from app.character.services import lists_service


@character.route('/add_chars', methods=['POST'])
def add_chars():
    data = request.json
    by = data['by']
    list_id = data.get('listId')
    char_ids = data.get('charIds')
    result = 'Done'
    if by == 'characters':
        chars = data.get('characters')
        result = lists_service.add_chars_to_list(list_id=list_id, chars=chars)
    elif by == 'ids':
        lists_service.add_chars_by_ids(list_id=list_id, char_ids=char_ids)
    return {'result': result}, 200
