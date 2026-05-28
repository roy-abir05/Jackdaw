from fastapi import APIRouter
from jackdaw.server.services.query_engine import QueryEngine
from jackdaw.server.services.anne import AnneEngine

router = APIRouter()

@router.get("/api/log/today")
def get_captains_log():
    raw_data = QueryEngine.get_daily_snapshot()
    ai_analysis = AnneEngine.generate_captains_log(raw_data)
    
    return {
        "status": "success",
        "data": raw_data,
        "ai_analysis": ai_analysis
    }