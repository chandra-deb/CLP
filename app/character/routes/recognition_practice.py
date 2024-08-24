from flask import request, redirect, url_for, render_template, jsonify, json

from app.character import character
from app.character.services import lists_service


@character.route('/recognition_practice', methods=['POST'])
def recognition_practice():
    # option = request.form['option']
    # value = request.form['value']
    # Use the option and value here

    list_id = request.form.get('list_id')
    words_size = request.form.get('size')
    time_length = request.form.get('time')
    category = request.form.get('category')
    print('Category', category)
    practice_type = 'by_words_size'
    characters = []
    if words_size is not None:
        if category == 'ns':
            characters = [char.to_json() for char in
                          lists_service.get_never_studied_chars_of_list(list_id=list_id, limit=words_size)]
        if category == 'ws':
            characters = [char.to_json() for char in
                          lists_service.get_weak_chars_of_list(list_id=list_id, limit=words_size)]

            print('length', len(characters))
        if category == 'ss':
            characters = [char.to_json() for char in
                          lists_service.get_strong_chars_of_list(list_id=list_id, limit=words_size)]

    elif time_length is not None:
        practice_type = 'by_time_length'
        if category == 'ns':
            characters = [char.to_json() for char in
                          lists_service.get_never_studied_chars_of_list(list_id=list_id, limit=None)]
        if category == 'ws':
            characters = [char.to_json() for char in
                          lists_service.get_weak_chars_of_list(list_id=list_id, limit=None)]
        if category == 'ss':
            characters = [char.to_json() for char in
                          lists_service.get_strong_chars_of_list(list_id=list_id, limit=None)]
    print("Words Size: ", words_size)
    print("List ID: ", list_id)

    return render_template('recognition_practice.html', characters=characters, time_length=time_length,
                           practice_type=practice_type)
