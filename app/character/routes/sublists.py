from flask import render_template
from flask_login import current_user

from app.character import character
from app.models import CharacterList
from app import db

def get_all_parents(list_id):
    # Create a CTE to recursively get all parents
    parent_cte = db.session.query(CharacterList).\
        filter(CharacterList.id == list_id).\
        cte(recursive=True)

    # Define the recursive query
    parent_cte = parent_cte.union_all(
        db.session.query(CharacterList).\
            filter(CharacterList.id == parent_cte.c.parent_list_id)
    )

    # Get all parents
    all_parents = db.session.query(parent_cte).all()

    # Return the parent list objects
    reversed_parents = all_parents[::-1]
    return reversed_parents[:-1]


@character.route('/lists/<int:list_id>')
def sublists(list_id):
    # Parent lists
    parents = get_all_parents(list_id)
    #

    current_list = CharacterList.query.get(list_id)
    if current_list is None:
        return 'List not found', 404
    child_lists = current_list.child_lists
    print(current_list.parent_list)
    print('Sublists: ')
    print(child_lists)

    print('Parents')
    print(parents)
    characters = current_list.characters
    return render_template('sublists.html', list=current_list, child_lists=child_lists, characters=characters,
                           parents=parents)
