from flask import render_template
from flask_login import login_required, current_user

from app import db
from app.character import character
from app.character.services import list_service
from app.models import CharacterList


# Revise 1
# !! This codes also works well
@character.route('/lists')
def lists():
    top_level_user_lists = db.session.scalars(
        db.select(CharacterList)
        .where(CharacterList.user_id == current_user.id)
        .where(CharacterList.parent_list == None)
    ).all()
    top_level_premade_lists = db.session.scalars(
        db.select(CharacterList)
        .where(CharacterList.is_admin_created == True)
        .where(CharacterList.parent_list == None)
    ).all()
    return render_template('lists.html', user_lists=top_level_user_lists, premade_lists=top_level_premade_lists)
