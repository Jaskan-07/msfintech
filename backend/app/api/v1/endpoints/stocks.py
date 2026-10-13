"""
Stocks & Market Watch Endpoints
Directly integrated with National Stock Exchange (NSE) MCP Server
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException

from app.schemas.stocks import MarketItem
from app.services.nse_service import NSEService

router = APIRouter()


@router.get("/market-watch", response_model=List[MarketItem])
def get_market_watch(
    category: Optional[str] = Query(
        "all",
        description="Filter items by category: 'all', 'indices', 'stocks', 'bonds', 'yields'"
    )
):
    """
    Get live market watch data matching the fintech widget view.
    Fetches live Indian stocks, indices, and yields from NSE MCP Server (cm-market).
    """
    service = NSEService.get_instance()
    items = service.get_market_watch(category=category or "all")
    return items


@router.get("/indices", response_model=List[MarketItem])
def get_live_indices():
    """Get live Indian market indices (NIFTY 50, NIFTY BANK, NIFTY IT, etc.) via NSE MCP."""
    service = NSEService.get_instance()
    return service.get_live_indices()


@router.get("/quote/{symbol}")
def get_stock_quote(symbol: str):
    """Get live quote for a specific stock (e.g. RELIANCE, TCS, INFY) via cm_get_stock_quote."""
    service = NSEService.get_instance()
    quote = service.get_stock_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail=f"Stock quote for '{symbol}' not found on NSE.")
    return quote


@router.get("/mcp/status")
def get_mcp_status():
    """Check connectivity and session status of configured NSE MCP servers."""
    service = NSEService.get_instance()
    return service.get_mcp_status()
