import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { API_BASE_URL } from '../../config/api'
import './MarketWatchWidget.css'

export interface MarketItem {
  symbol: string
  name: string
  value: number
  formatted_value: string
  change: number
  formatted_change: string
  pct_change: number
  direction: 'up' | 'down' | 'neutral'
  category: 'indices' | 'stocks' | 'bonds'
  unit?: string
  high?: number | null
  low?: number | null
  open?: number | null
  volume?: number | null
  timestamp?: string | null
}

export const MarketWatchWidget: React.FC = () => {
  const [items, setItems] = useState<MarketItem[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [category, setCategory] = useState<string>('all')
  const [lastUpdated, setLastUpdated] = useState<string>('')
  const [selectedItem, setSelectedItem] = useState<MarketItem | null>(null)
  const [error, setError] = useState<string | null>(null)

  const fetchMarketData = async (cat: string) => {
    try {
      setLoading(true)
      setError(null)
      const res = await axios.get(`${API_BASE_URL}/stocks/market-watch?category=${cat}`)
      setItems(res.data)
      setLastUpdated(new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }))
    } catch (err) {
      console.error('Failed to fetch market data:', err)
      setError('Unable to load live market data from NSE MCP server.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMarketData(category)
    const interval = setInterval(() => {
      fetchMarketData(category)
    }, 15000) // auto-refresh every 15s
    return () => clearInterval(interval)
  }, [category])

  return (
    <div className="market-watch-card">
      <div className="market-watch-header">
        <div className="title-area">
          <div className="title-row">
            <h3>Indian Markets & Stocks</h3>
            <span className="live-badge" title="Streaming via official NSE Model Context Protocol">
              <span className="pulsing-dot" /> NSE MCP LIVE
            </span>
          </div>
          <p className="subtitle">
            National Stock Exchange of India • Live Snapshots
            {lastUpdated && <span className="time-indicator"> • Updated {lastUpdated}</span>}
          </p>
        </div>
        <button
          className="refresh-btn"
          onClick={() => fetchMarketData(category)}
          disabled={loading}
          title="Refresh latest data"
        >
          {loading ? '↻ Loading...' : '↻ Refresh'}
        </button>
      </div>

      <div className="filter-tabs">
        <button
          className={`tab-btn ${category === 'all' ? 'active' : ''}`}
          onClick={() => setCategory('all')}
        >
          All
        </button>
        <button
          className={`tab-btn ${category === 'indices' ? 'active' : ''}`}
          onClick={() => setCategory('indices')}
        >
          Indices
        </button>
        <button
          className={`tab-btn ${category === 'stocks' ? 'active' : ''}`}
          onClick={() => setCategory('stocks')}
        >
          Indian Stocks
        </button>
        <button
          className={`tab-btn ${category === 'bonds' ? 'active' : ''}`}
          onClick={() => setCategory('bonds')}
        >
          10yr Yields & Bonds
        </button>
      </div>

      {error ? (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => fetchMarketData(category)}>Retry</button>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="market-table">
            <thead>
              <tr>
                <th className="col-name">NAME</th>
                <th className="col-val text-right">
                  {category === 'bonds' ? 'YIELD' : 'PRICE / VALUE'}
                </th>
                <th className="col-chg text-right">CHG</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => {
                const isUp = item.direction === 'up'
                const isDown = item.direction === 'down'
                const isSelected = selectedItem?.symbol === item.symbol

                return (
                  <React.Fragment key={item.symbol}>
                    <tr
                      className={`market-row ${isSelected ? 'row-selected' : ''}`}
                      onClick={() => setSelectedItem(isSelected ? null : item)}
                    >
                      <td className="cell-name">
                        <span className={`direction-arrow ${item.direction}`}>
                          {isUp && '↑'}
                          {isDown && '↓'}
                          {!isUp && !isDown && '—'}
                        </span>
                        <span className="item-name">{item.name}</span>
                        {item.symbol && item.name !== item.symbol && (
                          <span className="item-ticker">{item.symbol}</span>
                        )}
                      </td>
                      <td className="cell-val text-right">
                        <span className="value-text">{item.formatted_value}</span>
                        {item.unit === '%' && <span className="unit-label">%</span>}
                      </td>
                      <td className={`cell-chg text-right ${item.direction}`}>
                        <span className="chg-val">{item.formatted_change}</span>
                        <span className="pct-pill">
                          ({isUp ? '+' : ''}{item.pct_change.toFixed(2)}%)
                        </span>
                      </td>
                    </tr>
                    {isSelected && (
                      <tr className="detail-row">
                        <td colSpan={3}>
                          <div className="detail-drawer">
                            <div className="detail-stat">
                              <span className="stat-label">Open:</span>
                              <span className="stat-val">{item.open ? item.open.toLocaleString('en-IN') : '—'}</span>
                            </div>
                            <div className="detail-stat">
                              <span className="stat-label">High:</span>
                              <span className="stat-val text-green">{item.high ? item.high.toLocaleString('en-IN') : '—'}</span>
                            </div>
                            <div className="detail-stat">
                              <span className="stat-label">Low:</span>
                              <span className="stat-val text-red">{item.low ? item.low.toLocaleString('en-IN') : '—'}</span>
                            </div>
                            {item.volume ? (
                              <div className="detail-stat">
                                <span className="stat-label">Volume:</span>
                                <span className="stat-val">{item.volume.toLocaleString('en-IN')}</span>
                              </div>
                            ) : null}
                            <div className="detail-stat">
                              <span className="stat-label">Segment:</span>
                              <span className="stat-val">{item.category.toUpperCase()}</span>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      <div className="market-watch-footer">
        <span>Click any row for intraday stats • Connected to NSE MCP (Streamable HTTP)</span>
      </div>
    </div>
  )
}
