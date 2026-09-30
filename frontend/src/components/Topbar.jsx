import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { LogOut, User } from 'lucide-react';

const Topbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm z-10 relative">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">Military Asset Management System</h2>
      </div>
      
      <div className="flex items-center space-x-4">
        <div className="flex items-center text-sm font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full">
          <User size={16} className="mr-2 text-brand-teal" />
          {user?.fullName} ({user?.role})
        </div>
        <button 
          onClick={logout}
          className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors"
          title="Logout"
        >
          <LogOut size={20} />
        </button>
      </div>
    </header>
  );
};

export default Topbar;
