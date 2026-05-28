from fastapi import APIRouter
from jackdaw.server.services.coral import run_query

router = APIRouter()

@router.get("/api/test-data")
def get_test_commits():
    """
    Temporary endpoint for the frontend to verify the Coral connection.
    """
    # Using the correct schema pattern for GitHub queries
    sql = """
        SELECT sha, commit__author__name, commit__message 
        FROM github.commits 
        WHERE owner = 'withcoral' AND repo = 'coral' 
        LIMIT 5
    """
    data = run_query(sql)
    return {"status": "success", "data": data}