import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from '../features/auth/Login'
import Dashboard from '../features/dashboard/Dashboard'
import { AuthProvider } from '../shared/context/AuthContext'
import ProtectedRoute from '../shared/components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
