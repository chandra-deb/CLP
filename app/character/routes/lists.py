from flask import render_template
from flask_login import login_required, current_user

from app import db
from app.character import character
from app.character.services import list_service
from app.models import CharacterList


# Revise 2
# it is not working when different user create character list with same name.
# It just returns the very first list with the name.
# It can be solved by also using user id to filter
@character.route('/lists')
def lists():
    top_level_lists = db.session.scalars(
        db.select(CharacterList).where(CharacterList.parent_list == None)
        # .where(CharacterList.is_admin_created == True)
        # .where(CharacterList.user_id == current_user.id)
    ).all()
    return render_template('lists.html', lists=top_level_lists)
