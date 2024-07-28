from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select
from app.models import CharacterList


class ListsRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_list_by_id(self, list_id):
        stmt = select(CharacterList).filter_by(id=list_id)
        result = self.db.session.execute(stmt)
        result = result.scalars().one_or_none()
        print("Result: ", result)
        # return result.scalar_one_or_none()
        return result

    def get_all_parent_lists(self, list_id):
        # Create a CTE to recursively get all parents
        parent_cte = (self.db.session.query(CharacterList)
                      .filter(CharacterList.id == list_id)
                      .cte(recursive=True))
    
        # Define the recursive query
        parent_cte = parent_cte.union_all(
            self.db.session.query(CharacterList)
            .filter(CharacterList.id == parent_cte.c.parent_list_id)
        )
    
        # Get all parents
        all_parents = self.db.session.query(parent_cte).all()
    
        # Return the parent list objects
        reversed_parents = all_parents[::-1]
        return reversed_parents[:-1]

    def get_top_level_user_lists(self):
        top_level_user_lists = self.db.session.scalars(
            select(CharacterList)
            .where(CharacterList.user_id == current_user.id)
            .where(CharacterList.parent_list == None)
        ).all()
        return top_level_user_lists

    def get_top_level_premade_lists(self):
        top_level_premade_lists = self.db.session.scalars(
            select(CharacterList)
            .where(CharacterList.is_admin_created == True)
            .where(CharacterList.parent_list == None)
        ).all()
        return top_level_premade_lists

    # Even though this method use latest SqlAlchemy 2.x version
    # But for some weird reason it is just returning the ids of the lists not the lists object itself...
    # def get_all_parents(self, list_id):
    #     # Alias for the CharacterList table
    #     parent_alias = aliased(CharacterList)
    #
    #     # Create a CTE to recursively get all parents
    #     parent_cte = (
    #         select(CharacterList)
    #         .where(CharacterList.id == list_id)
    #         .cte(name="parent_cte", recursive=True)
    #     )
    #
    #     # Define the recursive query
    #     parent_cte = parent_cte.union_all(
    #         select(CharacterList)
    #         .where(CharacterList.id == parent_cte.c.parent_list_id)
    #     )
    #
    #     # Get all parents
    #     stmt = select(parent_cte)
    #     result = self.session.execute(stmt)
    #
    #     # Retrieve all parent CharacterList objects
    #     all_parents = result.scalars().all()
    #
    #     # Return the parent list objects in reverse order, excluding the last element
    #     reversed_parents = all_parents[::-1]
    #     return reversed_parents[:-1]

