from flask import render_template, abort
from flask_login import current_user
from flask_sqlalchemy.session import Session

from app.character import character
from app.models import CharacterList
from app import db


# Main Purpose are here
from app.character.routes.lists import lists
from app.character.routes.sublists import sublists


# Having some problems when using - in the name of lists
# Style 3
# @character.route('/<path:list_path>')
# def character_sublist(list_path):
#     list_path_parts = list_path.split('/')
#     current_list = CharacterList.query.filter_by(name=list_path_parts[0].replace('-', ' '), parent_list=None).first()
#     if current_list is None:
#         return 'List not found', 404
#     for part in list_path_parts[1:]:
#         current_list = [sublist for sublist in current_list.child_lists if sublist.name == part.replace('-', ' ')]
#         if not current_list:
#             return 'List not found', 404
#         current_list = current_list[0]
#     sublists = current_list.child_lists
#     characters = current_list.characters
#     return render_template('sublists.html', list=current_list, sublists=sublists, characters=characters,
#                            list_path=list_path)
#


# Revise 1
# !! This codes also works well
# @character.route('/list')
# def character_list():
#     top_level_lists = db.session.scalars(
#         db.select(CharacterList).where(CharacterList.parent_list == None)
#     ).all()
#     return render_template('character_list.html', lists=top_level_lists)
#
# @character.route('/list/<int:list_id>')
# def character_sublist(list_id):
#     current_list = CharacterList.query.get(list_id)
#     if current_list is None:
#         return 'List not found', 404
#     sublists = current_list.child_lists
#     characters = current_list.characters
#     return render_template('sublists.html', list=current_list, sublists=sublists, characters=characters)
