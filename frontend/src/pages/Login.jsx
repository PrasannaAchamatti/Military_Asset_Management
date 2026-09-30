import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Shield } from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('password');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    const result = await login(username, password);
    if (!result.success) {
      setError(result.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-brand-blue/20 blur-[120px]"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-brand-teal/20 blur-[120px]"></div>
      
      <div className="w-full max-w-md glass-panel rounded-2xl p-8 relative z-10">
        <div className="flex flex-col items-center mb-8">
          <div className="mb-4">
            <img src="/logo.jpg" alt="MAMS Logo" className="w-24 h-24 object-cover rounded-2xl shadow-xl shadow-brand-blue/20 border border-slate-200" />
          </div>
          <h1 className="text-3xl font-bold text-slate-800 tracking-tight">MAMS</h1>
          <p className="text-slate-500 mt-2 text-center">Military Asset Management System</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm mb-6 border border-red-100 flex items-start">
            <span className="mr-2">⚠️</span> {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
            <input 
              type="text" 
              className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent transition-all outline-none text-slate-800 placeholder-slate-400"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent transition-all outline-none text-slate-800 placeholder-slate-400"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-brand-navy hover:bg-slate-800 text-white font-medium py-2.5 rounded-lg transition-colors shadow-md disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center"
          >
            {isLoading ? (
              <span className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
            ) : (
              'Secure Login'
            )}
          </button>
        </form>
        
        <div className="mt-8 text-center text-xs text-slate-400">
          <p>Demo accounts: admin, commander, logistics (pw: password)</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
