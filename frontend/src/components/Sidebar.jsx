import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Shield, LayoutDashboard, Package, ShoppingCart, ArrowRightLeft, ClipboardCheck, Users, Activity } from 'lucide-react';

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const navItems = [
    { name: 'Dashboard', path: '/app', icon: <LayoutDashboard size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Inventory', path: '/app/inventory', icon: <Package size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Purchases', path: '/app/purchases', icon: <ShoppingCart size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Transfers', path: '/app/transfers', icon: <ArrowRightLeft size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Assignments', path: '/app/assignments', icon: <ClipboardCheck size={20} />, roles: ['ADMIN', 'BASE_COMMANDER'] },
    { name: 'Users', path: '/app/users', icon: <Users size={20} />, roles: ['ADMIN'] },
    { name: 'Audit Logs', path: '/app/audit-logs', icon: <Activity size={20} />, roles: ['ADMIN'] },
  ];

  return (
    <div className="w-64 bg-brand-navy min-h-screen text-slate-300 flex flex-col shadow-2xl z-20 relative transition-all duration-300">
      <div className="h-16 flex items-center px-6 border-b border-slate-700/50">
        <img src="/logo.jpg" alt="MAMS Logo" className="w-8 h-8 object-cover rounded-md mr-3 shadow-sm shadow-black/50" />
        <h1 className="text-xl font-bold tracking-wider text-white">MAMS</h1>
      </div>
      
      <div className="flex-1 py-6 px-3 space-y-1 overflow-y-auto">
        <div className="px-3 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Navigation</div>
        {navItems.filter(item => item.roles.includes(user?.role)).map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-3 py-2.5 rounded-lg transition-colors duration-200 group ${
                isActive 
                  ? 'bg-brand-blue/20 text-brand-accent font-medium' 
                  : 'hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <span className="mr-3">{item.icon}</span>
            {item.name}
          </NavLink>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
