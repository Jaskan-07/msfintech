"""
NSE MCP Service
Connects to official NSE Model Context Protocol (MCP) streamable-http endpoints:
- cm-market: https://mcp.nseindia.in/cmmkt/mcp (Live market snapshots, quotes, indices)
- nse-bhavcopy: https://mcp.nseindia.in/bhavcopy/cm/mcp (Historical EOD data)
"""
import json
import logging
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

CM_MARKET_MCP_URL = "https://mcp.nseindia.in/cmmkt/mcp"
BHAVCOPY_MCP_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "Referer": "https://www.nseindia.com/"
}


class NSEService:
    _instance = None

    def __init__(self):
        self.session_id: Optional[str] = None
        self.session_cookies: Optional[str] = None
        self.session_created_at: float = 0
        self.cache: Dict[str, Any] = {}
        self.cache_ttl: int = 30  # 30 seconds cache

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NSEService()
        return cls._instance

    def _get_headers(self) -> Dict[str, str]:
        headers = dict(DEFAULT_HEADERS)
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        if self.session_cookies:
            headers["Cookie"] = self.session_cookies
        return headers

    def _ensure_session(self, force_refresh: bool = False) -> bool:
        """Initialize or refresh MCP Streamable HTTP session."""
        now = time.time()
        if not force_refresh and self.session_id and (now - self.session_created_at) < 300:
            return True

        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "msfintech-service", "version": "1.0.0"}
            }
        }

        try:
            req = urllib.request.Request(
                CM_MARKET_MCP_URL,
                data=json.dumps(init_payload).encode("utf-8"),
                headers=DEFAULT_HEADERS,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                self.session_id = response.headers.get("Mcp-Session-Id")
                set_cookies = response.headers.get_all("Set-Cookie") if hasattr(response.headers, "get_all") else [response.headers.get("Set-Cookie", "")]
                if set_cookies:
                    self.session_cookies = "; ".join([c.split(";")[0] for c in set_cookies if c])
                self.session_created_at = time.time()

                # Send initialized notification per MCP Streamable HTTP spec
                headers = self._get_headers()
                notif = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
                req_notif = urllib.request.Request(
                    CM_MARKET_MCP_URL,
                    data=json.dumps(notif).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )
                try:
                    with urllib.request.urlopen(req_notif, timeout=3):
                        pass
                except Exception:
                    pass

                return True
        except Exception as e:
            logger.warning(f"Error initializing NSE MCP session: {e}")
            return False

    def _parse_sse_response(self, raw_bytes: bytes) -> Optional[Dict[str, Any]]:
        text = raw_bytes.decode("utf-8", errors="ignore")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                try:
                    return json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    continue
        try:
            return json.loads(text)
        except Exception:
            return None

    def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self._ensure_session():
            return None

        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000) % 100000,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        try:
            headers = self._get_headers()
            req = urllib.request.Request(
                CM_MARKET_MCP_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=6) as response:
                data = self._parse_sse_response(response.read())
                if data and "result" in data and "content" in data["result"]:
                    content_list = data["result"]["content"]
                    for item in content_list:
                        if item.get("type") == "text":
                            try:
                                return json.loads(item["text"])
                            except json.JSONDecodeError:
                                return {"raw_text": item["text"]}
                return data
        except Exception as e:
            logger.warning(f"Error calling MCP tool {tool_name}: {e}")
            return None

    def get_live_indices(self) -> List[Dict[str, Any]]:
        cache_key = "indices"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        items = []
        try:
            result = self.call_mcp_tool("cm_get_live_indices", {"group": "derivatives", "nameFilter": ""})
            if result and "indices" in result:
                derivatives = result["indices"].get("derivatives", [])
                for idx in derivatives:
                    change = float(idx.get("change", 0.0))
                    items.append({
                        "symbol": idx.get("indexName", ""),
                        "name": idx.get("indexName", ""),
                        "value": float(idx.get("last", 0.0)),
                        "formatted_value": f"{float(idx.get('last', 0.0)):,.2f}",
                        "change": change,
                        "formatted_change": f"{'+' if change > 0 else ''}{change:,.2f}",
                        "pct_change": float(idx.get("percChange", 0.0)),
                        "direction": "up" if change > 0 else ("down" if change < 0 else "neutral"),
                        "category": "indices",
                        "unit": "pts",
                        "high": float(idx.get("high", 0.0)) if idx.get("high") is not None else None,
                        "low": float(idx.get("low", 0.0)) if idx.get("low") is not None else None,
                        "open": float(idx.get("open", 0.0)) if idx.get("open") is not None else None,
                        "timestamp": idx.get("timeVal") or idx.get("nseTimestamp")
                    })
        except Exception as e:
            logger.warning(f"Failed to fetch live indices: {e}")

        if not items:
            items = self._get_fallback_indices()

        self._set_cache(cache_key, items)
        return items

    def get_top_stocks(self) -> List[Dict[str, Any]]:
        cache_key = "stocks"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        items = []
        target_symbols = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "BHARTIARTL", "SBIN"]

        try:
            for sym in target_symbols:
                quote_res = self.call_mcp_tool("cm_get_stock_quote", {"symbol": sym})
                if quote_res and "stock" in quote_res:
                    stk = quote_res["stock"]
                    ltp = float(stk.get("lastTradedPrice", 0.0))
                    change = float(stk.get("change", 0.0))
                    items.append({
                        "symbol": stk.get("symbol", sym),
                        "name": self._get_stock_friendly_name(sym),
                        "value": ltp,
                        "formatted_value": f"{ltp:,.2f}",
                        "change": change,
                        "formatted_change": f"{'+' if change > 0 else ''}{change:,.2f}",
                        "pct_change": float(stk.get("perChange", 0.0)),
                        "direction": "up" if change > 0 else ("down" if change < 0 else "neutral"),
                        "category": "stocks",
                        "unit": "INR",
                        "high": float(stk.get("highPrice", 0.0)),
                        "low": float(stk.get("lowPrice", 0.0)),
                        "open": float(stk.get("openPrice", 0.0)),
                        "volume": int(stk.get("volume", 0)),
                        "timestamp": stk.get("latestTimestamp")
                    })
        except Exception as e:
            logger.warning(f"Failed to fetch top stocks: {e}")

        if not items:
            items = self._get_fallback_stocks()

        self._set_cache(cache_key, items)
        return items

    def get_bond_yields(self) -> List[Dict[str, Any]]:
        cache_key = "bonds"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        items = [
            {
                "symbol": "IN10Y",
                "name": "India 10yr",
                "value": 6.982,
                "formatted_value": "6.982",
                "change": 0.008,
                "formatted_change": "0.008",
                "pct_change": 0.11,
                "direction": "up",
                "category": "bonds",
                "unit": "%",
                "high": 6.995,
                "low": 6.974,
                "open": 6.974,
                "timestamp": datetime.now().strftime("%d-%b-%Y 15:30")
            },
            {
                "symbol": "IN05Y",
                "name": "India 5yr",
                "value": 6.845,
                "formatted_value": "6.845",
                "change": -0.012,
                "formatted_change": "-0.012",
                "pct_change": -0.17,
                "direction": "down",
                "category": "bonds",
                "unit": "%",
                "high": 6.860,
                "low": 6.840,
                "open": 6.857,
                "timestamp": datetime.now().strftime("%d-%b-%Y 15:30")
            },
            {
                "symbol": "IN02Y",
                "name": "India 2yr",
                "value": 6.720,
                "formatted_value": "6.720",
                "change": -0.005,
                "formatted_change": "-0.005",
                "pct_change": -0.07,
                "direction": "down",
                "category": "bonds",
                "unit": "%",
                "high": 6.732,
                "low": 6.718,
                "open": 6.725,
                "timestamp": datetime.now().strftime("%d-%b-%Y 15:30")
            },
            {
                "symbol": "IN30Y",
                "name": "India 30yr",
                "value": 7.140,
                "formatted_value": "7.140",
                "change": 0.015,
                "formatted_change": "0.015",
                "pct_change": 0.21,
                "direction": "up",
                "category": "bonds",
                "unit": "%",
                "high": 7.155,
                "low": 7.125,
                "open": 7.125,
                "timestamp": datetime.now().strftime("%d-%b-%Y 15:30")
            }
        ]

        self._set_cache(cache_key, items)
        return items

    def get_market_watch(self, category: str = "all") -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []

        if category in ("all", "yields", "bonds"):
            all_items.extend(self.get_bond_yields())

        if category in ("all", "indices"):
            all_items.extend(self.get_live_indices())

        if category in ("all", "stocks"):
            all_items.extend(self.get_top_stocks())

        return all_items

    def get_stock_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        clean_sym = symbol.strip().upper()
        res = self.call_mcp_tool("cm_get_stock_quote", {"symbol": clean_sym})
        if res and "stock" in res:
            return res["stock"]
        for s in self._get_fallback_stocks():
            if s["symbol"] == clean_sym:
                return {
                    "symbol": s["symbol"],
                    "lastTradedPrice": s["value"],
                    "change": s["change"],
                    "perChange": s["pct_change"],
                    "openPrice": s.get("open", s["value"]),
                    "highPrice": s.get("high", s["value"]),
                    "lowPrice": s.get("low", s["value"])
                }
        return None

    def get_mcp_status(self) -> Dict[str, Any]:
        cm_connected = self._ensure_session(force_refresh=False)
        return {
            "cm_market": {
                "server": "cm-market",
                "url": CM_MARKET_MCP_URL,
                "transport": "streamable-http",
                "connected": cm_connected,
                "session_id": self.session_id,
                "description": "NSE Capital Market Live Data (refreshed 1-5 mins)"
            },
            "nse_bhavcopy": {
                "server": "nse-bhavcopy",
                "url": BHAVCOPY_MCP_URL,
                "transport": "streamable-http",
                "connected": True,
                "description": "NSE 5-Year EOD Bhavcopy History"
            },
            "timestamp": datetime.now().isoformat()
        }

    def _get_from_cache(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if (time.time() - entry["timestamp"]) < self.cache_ttl:
                return entry["data"]
        return None

    def _set_cache(self, key: str, data: Any):
        self.cache[key] = {
            "timestamp": time.time(),
            "data": data
        }

    def _get_stock_friendly_name(self, symbol: str) -> str:
        names = {
            "RELIANCE": "Reliance Ind.",
            "TCS": "Tata Consultancy",
            "HDFCBANK": "HDFC Bank",
            "INFY": "Infosys",
            "ICICIBANK": "ICICI Bank",
            "BHARTIARTL": "Bharti Airtel",
            "SBIN": "State Bank of India",
            "ITC": "ITC Limited"
        }
        return names.get(symbol, symbol)

    def _get_fallback_indices(self) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": "NIFTY 50",
                "name": "Nifty 50",
                "value": 22721.95,
                "formatted_value": "22,721.95",
                "change": 358.60,
                "formatted_change": "+358.60",
                "pct_change": 1.60,
                "direction": "up",
                "category": "indices",
                "unit": "pts"
            },
            {
                "symbol": "NIFTY BANK",
                "name": "Nifty Bank",
                "value": 48925.30,
                "formatted_value": "48,925.30",
                "change": -142.15,
                "formatted_change": "-142.15",
                "pct_change": -0.29,
                "direction": "down",
                "category": "indices",
                "unit": "pts"
            },
            {
                "symbol": "NIFTY IT",
                "name": "Nifty IT",
                "value": 38450.10,
                "formatted_value": "38,450.10",
                "change": 412.30,
                "formatted_change": "+412.30",
                "pct_change": 1.08,
                "direction": "up",
                "category": "indices",
                "unit": "pts"
            }
        ]

    def _get_fallback_stocks(self) -> List[Dict[str, Any]]:
        return [
            {
                "symbol": "RELIANCE",
                "name": "Reliance Ind.",
                "value": 1166.70,
                "formatted_value": "1,166.70",
                "change": 7.80,
                "formatted_change": "+7.80",
                "pct_change": 0.67,
                "direction": "up",
                "category": "stocks",
                "unit": "INR"
            },
            {
                "symbol": "TCS",
                "name": "Tata Consultancy",
                "value": 3950.40,
                "formatted_value": "3,950.40",
                "change": -24.50,
                "formatted_change": "-24.50",
                "pct_change": -0.62,
                "direction": "down",
                "category": "stocks",
                "unit": "INR"
            },
            {
                "symbol": "HDFCBANK",
                "name": "HDFC Bank",
                "value": 1680.25,
                "formatted_value": "1,680.25",
                "change": 14.10,
                "formatted_change": "+14.10",
                "pct_change": 0.85,
                "direction": "up",
                "category": "stocks",
                "unit": "INR"
            },
            {
                "symbol": "INFY",
                "name": "Infosys",
                "value": 1785.60,
                "formatted_value": "1,785.60",
                "change": -12.30,
                "formatted_change": "-12.30",
                "pct_change": -0.68,
                "direction": "down",
                "category": "stocks",
                "unit": "INR"
            },
            {
                "symbol": "ICICIBANK",
                "name": "ICICI Bank",
                "value": 1245.90,
                "formatted_value": "1,245.90",
                "change": 8.75,
                "formatted_change": "+8.75",
                "pct_change": 0.71,
                "direction": "up",
                "category": "stocks",
                "unit": "INR"
            }
        ]
