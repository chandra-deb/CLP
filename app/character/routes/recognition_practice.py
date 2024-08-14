from flask import request, redirect, url_for, render_template, jsonify, json

from app.character import character
from app.character.services import lists_service


@character.route('/recognition_practice', methods=['POST'])
def recognition_practice():
    # option = request.form['option']
    # value = request.form['value']
    # Use the option and value here
    words_size = request.form.get('size')
    list_id = request.form.get('list_id')
    print("Words Size: ", words_size)
    print("List ID: ", list_id)
    characters = [char.to_json() for char in
                  lists_service.get_never_studied_chars_of_list(list_id=list_id, limit=words_size)]
    return render_template('recognition_practice.html', characters=characters)
