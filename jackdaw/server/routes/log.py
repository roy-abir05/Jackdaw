from fastapi import APIRouter
from jackdaw.server.services.query_engine import QueryEngine
from jackdaw.server.services.anne import AnneEngine

router = APIRouter()

@router.get("/api/log/today")
def get_captains_log():

    unified_data = QueryEngine.get_code_to_cash_metrics()
    ai_analysis = AnneEngine.generate_captains_log(unified_data)
    
    return {
        "status": "success",
        "data": unified_data,
        "ai_analysis": ai_analysis
    }