import os

frontend_src = "f:/Military_Manage/frontend/src"

app_jsx = """import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Inventory from './pages/Inventory';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="inventory" element={<Inventory />} />
            <Route path="purchases" element={<div>Purchases</div>} />
            <Route path="transfers" element={<div>Transfers</div>} />
            <Route path="assignments" element={<div>Assignments & Expenditures</div>} />
            <Route path="users" element={<ProtectedRoute roles={['ADMIN']}><div>User Management</div></ProtectedRoute>} />
            <Route path="audit-logs" element={<ProtectedRoute roles={['ADMIN']}><div>Audit Logs</div></ProtectedRoute>} />
          </Route>
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
"""

sidebar = """import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Shield, LayoutDashboard, Package, ShoppingCart, ArrowRightLeft, ClipboardCheck, Users, Activity } from 'lucide-react';

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Inventory', path: '/inventory', icon: <Package size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Purchases', path: '/purchases', icon: <ShoppingCart size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Transfers', path: '/transfers', icon: <ArrowRightLeft size={20} />, roles: ['ADMIN', 'BASE_COMMANDER', 'LOGISTICS_OFFICER'] },
    { name: 'Assignments', path: '/assignments', icon: <ClipboardCheck size={20} />, roles: ['ADMIN', 'BASE_COMMANDER'] },
    { name: 'Users', path: '/users', icon: <Users size={20} />, roles: ['ADMIN'] },
    { name: 'Audit Logs', path: '/audit-logs', icon: <Activity size={20} />, roles: ['ADMIN'] },
  ];

  return (
    <div className="w-64 bg-brand-navy min-h-screen text-slate-300 flex flex-col shadow-2xl z-20 relative transition-all duration-300">
      <div className="h-16 flex items-center px-6 border-b border-slate-700/50">
        <Shield className="text-brand-accent mr-3" size={28} />
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
"""

topbar = """import React, { useContext } from 'react';
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
"""

layout = """import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

const Layout = () => {
  return (
    <div className="flex h-screen bg-brand-light overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar />
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <div className="max-w-7xl mx-auto animate-fade-in-up">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
"""

login_page = """import React, { useState, useContext } from 'react';
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
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-brand-blue/20 blur-[120px]"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-brand-teal/20 blur-[120px]"></div>
      
      <div className="w-full max-w-md glass-panel rounded-2xl p-8 relative z-10">
        <div className="flex flex-col items-center mb-8">
          <div className="bg-brand-navy p-4 rounded-full mb-4 shadow-lg border border-slate-700">
            <Shield className="text-brand-accent" size={48} />
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
"""

dashboard_page = """import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { Package, ShoppingCart, ArrowRightLeft, ClipboardCheck, ArrowDownToLine, ArrowUpFromLine } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const StatCard = ({ title, value, icon, color }) => (
  <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-100 flex items-center justify-between hover:shadow-md transition-shadow group cursor-default">
    <div>
      <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
      <h3 className="text-3xl font-bold text-slate-800 group-hover:text-brand-blue transition-colors">{value}</h3>
    </div>
    <div className={`p-4 rounded-full ${color} bg-opacity-10 text-current`}>
      {icon}
    </div>
  </div>
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/dashboard');
        setStats(response.data);
      } catch (error) {
        console.error('Failed to fetch dashboard stats', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="h-full flex items-center justify-center">Loading dashboard...</div>;

  const chartData = [
    { name: 'Purchases', value: stats?.purchases || 0 },
    { name: 'Transfer In', value: stats?.transferIn || 0 },
    { name: 'Transfer Out', value: stats?.transferOut || 0 },
    { name: 'Assigned', value: stats?.assigned || 0 },
    { name: 'Expended', value: stats?.expended || 0 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Logistics Overview</h1>
          <p className="text-slate-500 text-sm mt-1">Real-time tracking of military assets and inventory.</p>
        </div>
        
        <div className="bg-white px-4 py-2 rounded-lg shadow-sm border border-slate-200 text-sm font-medium">
          <span className="text-slate-500 mr-2">Net Movement:</span>
          <span className={`text-lg ${stats?.netMovement > 0 ? 'text-green-600' : stats?.netMovement < 0 ? 'text-red-600' : 'text-slate-700'}`}>
            {stats?.netMovement > 0 ? '+' : ''}{stats?.netMovement}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard title="Total Purchases" value={stats?.purchases || 0} icon={<ShoppingCart size={24} className="text-blue-500" />} color="bg-blue-500" />
        <StatCard title="Transfer In" value={stats?.transferIn || 0} icon={<ArrowDownToLine size={24} className="text-teal-500" />} color="bg-teal-500" />
        <StatCard title="Transfer Out" value={stats?.transferOut || 0} icon={<ArrowUpFromLine size={24} className="text-orange-500" />} color="bg-orange-500" />
        <StatCard title="Assigned/Expended" value={(stats?.assigned || 0) + (stats?.expended || 0)} icon={<ClipboardCheck size={24} className="text-red-500" />} color="bg-red-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-semibold text-slate-800 mb-6">Movement Analytics</h3>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b'}} />
                <Tooltip 
                  cursor={{fill: '#f1f5f9'}}
                  contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} maxBarSize={50} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-brand-navy rounded-xl shadow-lg p-6 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-brand-accent opacity-10 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2"></div>
          
          <h3 className="text-lg font-semibold mb-6 flex items-center">
            <Package className="mr-2 text-brand-accent" size={20} />
            Inventory Status
          </h3>
          
          <div className="space-y-6">
            <div>
              <p className="text-slate-400 text-sm mb-1">Opening Balance</p>
              <p className="text-2xl font-semibold">{stats?.openingBalance || 0}</p>
            </div>
            
            <div className="w-full h-px bg-slate-700"></div>
            
            <div>
              <p className="text-slate-400 text-sm mb-1">Closing Balance</p>
              <p className="text-4xl font-bold text-brand-accent">{stats?.closingBalance || 0}</p>
            </div>
          </div>
          
          <div className="mt-8 text-xs text-slate-400 leading-relaxed">
            * Closing balance represents the current available physical inventory after all recorded movements.
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
"""

inventory_page = """import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { Package, Search, Filter } from 'lucide-react';

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const res = await api.get('/inventory');
        setInventory(res.data);
      } catch (error) {
        console.error("Failed to fetch inventory", error);
      } finally {
        setLoading(false);
      }
    };
    fetchInventory();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <Package className="mr-3 text-brand-blue" />
          Current Inventory
        </h1>
        
        <div className="flex space-x-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text" 
              placeholder="Search assets..." 
              className="pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent w-64"
            />
          </div>
          <button className="flex items-center px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors">
            <Filter size={16} className="mr-2" />
            Filters
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full whitespace-nowrap">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Base</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Equipment Code</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Name</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Category</th>
                <th className="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">Quantity</th>
                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-slate-500">Loading inventory data...</td></tr>
              ) : inventory.length === 0 ? (
                <tr><td colSpan="6" className="px-6 py-8 text-center text-slate-500">No inventory found</td></tr>
              ) : (
                inventory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 text-sm text-slate-800 font-medium">{item.base.baseName}</td>
                    <td className="px-6 py-4 text-sm text-slate-500 font-mono bg-slate-50 rounded-md my-2 inline-block px-2 ml-4">{item.equipmentType.equipmentCode}</td>
                    <td className="px-6 py-4 text-sm text-slate-800">{item.equipmentType.equipmentName}</td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-600">
                        {item.equipmentType.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-800 font-semibold text-right">{item.quantity} <span className="text-slate-400 font-normal text-xs ml-1">{item.equipmentType.unit}</span></td>
                    <td className="px-6 py-4 text-sm text-center">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                        item.quantity > 50 ? 'bg-green-100 text-green-700' : 
                        item.quantity > 10 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
                      }`}>
                        {item.quantity > 50 ? 'Healthy' : item.quantity > 10 ? 'Low' : 'Critical'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Inventory;
"""

with open(f"{frontend_src}/App.jsx", "w", encoding="utf-8") as f: f.write(app_jsx)
with open(f"{frontend_src}/components/Sidebar.jsx", "w", encoding="utf-8") as f: f.write(sidebar)
with open(f"{frontend_src}/components/Topbar.jsx", "w", encoding="utf-8") as f: f.write(topbar)
with open(f"{frontend_src}/components/Layout.jsx", "w", encoding="utf-8") as f: f.write(layout)
with open(f"{frontend_src}/pages/Login.jsx", "w", encoding="utf-8") as f: f.write(login_page)
with open(f"{frontend_src}/pages/Dashboard.jsx", "w", encoding="utf-8") as f: f.write(dashboard_page)
with open(f"{frontend_src}/pages/Inventory.jsx", "w", encoding="utf-8") as f: f.write(inventory_page)

print("React app scaffolded successfully.")
