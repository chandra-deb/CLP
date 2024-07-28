from app.account.repositories.dashboard_repository import DashboardRepository
from app.account.services.dashboard_service import DashboardService
from app import db

dashboard_service = DashboardService(DashboardRepository(db))
