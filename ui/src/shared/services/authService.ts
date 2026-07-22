import axios from 'axios'
import { API_BASE_URL } from '../../config/api'

interface UserResponse {
  id: string
  username: string
  email: string
  full_name?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export const authService = {
  async login(username: string, password: string): Promise<UserResponse> {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, {
      username,
      password
    })
    return response.data
  },

  async register(
    username: string,
    email: string,
    password: string,
    fullName?: string
  ) {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      email,
      password,
      full_name: fullName
    })
    return response.data
  },

  getSession(): string | null {
    return localStorage.getItem('auth_user')
  },

  setSession(user: UserResponse): void {
    localStorage.setItem('auth_user', JSON.stringify(user))
  },

  removeSession(): void {
    localStorage.removeItem('auth_user')
  },

  isAuthenticated(): boolean {
    return !!this.getSession()
  }
}
