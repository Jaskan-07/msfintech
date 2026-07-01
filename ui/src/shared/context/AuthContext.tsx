import { createContext, useContext, useState, ReactNode } from 'react'
import { authService } from '../services/authService'

interface AuthContextType {
  isAuthenticated: boolean
  session: string | null
  login: (user: any) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<string | null>(authService.getSession())

  const login = (user: any) => {
    authService.setSession(user)
    setSession(JSON.stringify(user))
  }

  const logout = () => {
    authService.removeSession()
    setSession(null)
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!session,
        session,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
