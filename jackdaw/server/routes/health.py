from fastapi import APIRouter
from jackdaw.server.services.query_engine import QueryEngine

router = APIRouter()

@router.get("/api/health")
def get_dashboard_health():
    """
    Returns the aggregated daily snapshot to power the web dashboard.
    """
    try:
        data = QueryEngine.get_daily_snapshot()
        return {
            "status": "success",
            "dashboard_data": {
                "latest_deployments": data
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}