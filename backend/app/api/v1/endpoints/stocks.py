import httpx
from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings

router = APIRouter()

@router.get("/live-overview")
async def get_stock_overview(
    identifier: str = Query(..., description="The stock ISIN or ticker code, e.g., US5949181045")
):
    """
    Fetch live financial profile and market metrics from the Eulerpool API
    """
    # Eulerpool API Base URL: https://api.eulerpool.com
    cleaned_id = identifier.strip('/')
    if cleaned_id.startswith("api/"):
        url = f"https://api.eulerpool.com/{cleaned_id}"
    else:
        url = f"https://api.eulerpool.com/api/1/equity/overview/{cleaned_id}"
    
    headers = {
        "Authorization": f"Bearer {settings.EULERPOOL_API_KEY}",
        "Accept": "application/json",
        "User-Agent": "MSFinTech-Dashboard/1.0"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            
            # Check for API key / authorization failures (HTTP 401 / 403)
            if response.status_code in (401, 403):
                raise HTTPException(status_code=500, detail="Eulerpool API key authentication failed.")
            elif response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Eulerpool.")
                
            return response.json()
            
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"External financial network unreachable: {exc}")
