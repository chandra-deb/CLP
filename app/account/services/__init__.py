from app.account.repositories.dashboard_repository import DashboardRepository
from app.account.services.dashboard_service import DashboardService

dashboard_service = DashboardService(DashboardRepository())