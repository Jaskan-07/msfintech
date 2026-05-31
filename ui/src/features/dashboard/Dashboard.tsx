import { useAuth } from '../../shared/context/AuthContext'
import { useNavigate } from 'react-router-dom'
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
        <div className="welcome-card">
          <h2>Welcome!</h2>
          <p>You have successfully logged in.</p>
          <p>Dashboard features coming soon...</p>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
