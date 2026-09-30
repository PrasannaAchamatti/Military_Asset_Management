import React, { useState, useEffect } from 'react';
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
