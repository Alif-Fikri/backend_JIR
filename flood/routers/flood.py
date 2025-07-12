from fastapi import APIRouter, HTTPException
from flood.services.flood import fetch_flood_data

router = APIRouter(prefix="/api/flood", tags=["flood"])

@router.get("/data")
async def get_flood_data():
    try:
        data = await fetch_flood_data()
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
