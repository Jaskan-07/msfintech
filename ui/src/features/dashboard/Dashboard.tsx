import { useAuth } from '../../shared/context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { MarketWatchWidget } from './MarketWatchWidget'
import './Dashboard.css'

function Dashboard() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Economic Indicators Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="dashboard-content">
        <MarketWatchWidget />
      </main>
    </div>
  )
}

export default Dashboard
