import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import { Users as UsersIcon, Plus, X } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Users = () => {
  const { user } = useContext(AuthContext);
  const [users, setUsers] = useState([]);
  const [bases, setBases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    fullName: '',
    email: '',
    role: 'LOGISTICS_OFFICER',
    baseId: ''
  });

  const fetchData = async () => {
    try {
      const usersRes = await api.get('/users').catch(e => {
        console.error("Failed to fetch users", e);
        return { data: [] };
      });
      const basesRes = await api.get('/bases').catch(e => {
        console.error("Failed to fetch bases", e);
        return { data: [] };
      });
      
      setUsers(usersRes.data);
      setBases(basesRes.data);
    } catch (error) {
      console.error("Error in fetchData", error);
    }
  };

  useEffect(() => {
    if(user.role === 'ADMIN') fetchData();
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/users', formData);
      setShowForm(false);
      fetchData();
    } catch (error) {
      alert("Error adding user");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <UsersIcon className="mr-3 text-brand-navy" />
          User Management
        </h1>
        <button 
          onClick={() => setShowForm(true)}
          className="bg-brand-navy text-white px-4 py-2 rounded-lg font-medium hover:bg-slate-800 transition-colors flex items-center"
        >
          <Plus size={18} className="mr-2" /> Add User
        </button>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h2 className="text-lg font-bold text-slate-700">Add New User</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-400"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
                <input required type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, fullName: e.target.value})} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
                  <input required type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, username: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                  <input required type="password" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, password: e.target.value})} />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                <input required type="email" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, email: e.target.value})} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Role</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, role: e.target.value})}>
                    <option value="LOGISTICS_OFFICER">Logistics Officer</option>
                    <option value="BASE_COMMANDER">Base Commander</option>
                    <option value="ADMIN">Admin</option>
                  </select>
                </div>
                {formData.role !== 'ADMIN' && (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Base</label>
                    <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, baseId: e.target.value})}>
                      <option value="">Select Base</option>
                      {bases.map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                    </select>
                  </div>
                )}
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-slate-600 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-brand-navy text-white rounded-lg font-medium">Create User</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Name</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Username</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Role</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Base ID</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {users.map(u => (
              <tr key={u.id} className="hover:bg-slate-50">
                <td className="px-6 py-4 font-medium text-slate-800">{u.fullName}</td>
                <td className="px-6 py-4 font-mono text-sm text-slate-500">{u.username}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    u.role === 'ADMIN' ? 'bg-purple-100 text-purple-700' :
                    u.role === 'BASE_COMMANDER' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-700'
                  }`}>{u.role}</span>
                </td>
                <td className="px-6 py-4 text-slate-500">{u.baseId || 'Global'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;
