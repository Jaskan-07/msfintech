import axios from 'axios'
import { API_BASE_URL } from '../../config/api'

interface LoginResponse {
  access_token: string
  token_type: string
}

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
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

  getToken(): string | null {
    return localStorage.getItem('token')
  },

  setToken(token: string): void {
    localStorage.setItem('token', token)
  },

  removeToken(): void {
    localStorage.removeItem('token')
  },

  isAuthenticated(): boolean {
    return !!this.getToken()
  }
}
