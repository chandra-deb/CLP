from app import db
from app.character.repositories.lists_repository import ListsRepository
from app.character.services.lists_service import ListsService

lists_service = ListsService(ListsRepository(db))
