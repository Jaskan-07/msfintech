"""
Schemas for NSE Stock & Market Data
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class MarketItem(BaseModel):
    symbol: str
    name: str
    value: float
    formatted_value: str
    change: float
    formatted_change: str
    pct_change: float
    direction: str  # 'up', 'down', 'neutral'
    category: str   # 'indices', 'stocks', 'bonds'
    unit: str = ""   # e.g., 'INR', '%', 'pts'
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    volume: Optional[int] = None
    timestamp: Optional[str] = None


class MarketWatchResponse(BaseModel):
    timestamp: str
    source: str
    items: List[MarketItem]


class StockQuote(BaseModel):
    symbol: str
    series: Optional[str] = None
    last_traded_price: float
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    prev_close_price: Optional[float] = None
    change: float
    per_change: float
    volume: Optional[int] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    latest_timestamp: Optional[str] = None


class MCPStatusResponse(BaseModel):
    connected: bool
    server: str
    endpoint: str
    transport: str
    active_tools_count: int
    last_ping: str
    details: Optional[Dict[str, Any]] = None
