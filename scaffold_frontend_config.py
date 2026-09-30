import os

frontend_root = "f:/Military_Manage/frontend"
frontend_src = f"{frontend_root}/src"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir(f"{frontend_src}/context")
ensure_dir(f"{frontend_src}/api")
ensure_dir(f"{frontend_src}/components")
ensure_dir(f"{frontend_src}/pages")

# Tailwind config
tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#0f172a',
          charcoal: '#1e293b',
          light: '#f8fafc',
          blue: '#3b82f6',
          teal: '#14b8a6',
          accent: '#0ea5e9',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
"""

index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-brand-light text-slate-800 font-sans antialiased;
  }
}

.glass-panel {
  @apply bg-white bg-opacity-90 backdrop-blur-md border border-white border-opacity-20 shadow-xl;
}
"""

axios_config = """import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
"""

auth_context = """import React, { createContext, useState, useEffect } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const { accessToken, user } = response.data;
      
      localStorage.setItem('token', accessToken);
      localStorage.setItem('user', JSON.stringify(user));
      
      setUser(user);
      navigate('/');
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.message || 'Login failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
"""

protected_route = """import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const ProtectedRoute = ({ children, roles }) => {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;

  return children;
};

export default ProtectedRoute;
"""

with open(f"{frontend_root}/tailwind.config.js", "w") as f: f.write(tailwind_config)
with open(f"{frontend_src}/index.css", "w") as f: f.write(index_css)
with open(f"{frontend_src}/api/axios.js", "w") as f: f.write(axios_config)
with open(f"{frontend_src}/context/AuthContext.jsx", "w") as f: f.write(auth_context)
with open(f"{frontend_src}/components/ProtectedRoute.jsx", "w") as f: f.write(protected_route)

print("Frontend configuration generated.")
