import os

frontend_src = "f:/Military_Manage/frontend/src"

pages = {
    "Purchases.jsx": """import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import { ShoppingCart, Plus, X } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Purchases = () => {
  const { user } = useContext(AuthContext);
  const [purchases, setPurchases] = useState([]);
  const [equipmentTypes, setEquipmentTypes] = useState([]);
  const [bases, setBases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    equipmentTypeId: '',
    quantity: '',
    baseId: '',
    supplier: '',
    referenceNumber: '',
    remarks: ''
  });

  const fetchData = async () => {
    try {
      const [purchasesRes, equipmentRes, basesRes] = await Promise.all([
        api.get('/purchases' + (user.role !== 'ADMIN' ? `?baseId=${user.baseId}` : '')),
        api.get('/equipment-types'),
        api.get('/bases')
      ]);
      setPurchases(purchasesRes.data);
      setEquipmentTypes(equipmentRes.data);
      setBases(basesRes.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/purchases', {
        ...formData,
        quantity: parseInt(formData.quantity),
        baseId: user.role !== 'ADMIN' ? user.baseId : parseInt(formData.baseId)
      });
      setShowForm(false);
      fetchData();
    } catch (error) {
      console.error("Error adding purchase", error);
      alert("Failed to add purchase");
    }
  };

  return (
    <div className="space-y-6 relative">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ShoppingCart className="mr-3 text-brand-blue" />
          Purchases
        </h1>
        <button 
          onClick={() => setShowForm(true)}
          className="bg-brand-blue text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-accent transition-colors flex items-center"
        >
          <Plus size={18} className="mr-2" /> New Purchase
        </button>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h2 className="text-lg font-bold text-slate-700">Record New Purchase</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-400 hover:text-slate-600"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Equipment</label>
                <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, equipmentTypeId: e.target.value})}>
                  <option value="">Select Equipment</option>
                  {equipmentTypes.map(eq => <option key={eq.id} value={eq.id}>{eq.equipmentName} ({eq.equipmentCode})</option>)}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Quantity</label>
                  <input required type="number" min="1" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, quantity: e.target.value})} />
                </div>
                {user.role === 'ADMIN' && (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Target Base</label>
                    <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, baseId: e.target.value})}>
                      <option value="">Select Base</option>
                      {bases.map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                    </select>
                  </div>
                )}
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Supplier</label>
                  <input type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, supplier: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Reference No.</label>
                  <input type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, referenceNumber: e.target.value})} />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Remarks</label>
                <textarea className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, remarks: e.target.value})}></textarea>
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-slate-600 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-brand-blue text-white rounded-lg font-medium">Save Purchase</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Date</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Equipment</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Qty</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Base</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Supplier</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {purchases.map(p => (
              <tr key={p.id}>
                <td className="px-6 py-4 text-sm text-slate-600">{p.purchaseDate}</td>
                <td className="px-6 py-4 text-sm font-medium text-slate-800">{p.equipmentType.equipmentName}</td>
                <td className="px-6 py-4 text-sm font-bold text-slate-800">{p.quantity}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{p.base.baseName}</td>
                <td className="px-6 py-4 text-sm text-slate-600">{p.supplier}</td>
              </tr>
            ))}
            {purchases.length === 0 && (
              <tr><td colSpan="5" className="text-center py-8 text-slate-500">No purchases found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Purchases;
""",

    "Transfers.jsx": """import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import { ArrowRightLeft, Plus, X, Check, PackageCheck } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Transfers = () => {
  const { user } = useContext(AuthContext);
  const [transfers, setTransfers] = useState([]);
  const [equipmentTypes, setEquipmentTypes] = useState([]);
  const [bases, setBases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    equipmentTypeId: '',
    quantity: '',
    fromBaseId: '',
    toBaseId: '',
    remarks: ''
  });

  const fetchData = async () => {
    try {
      const [transfersRes, equipmentRes, basesRes] = await Promise.all([
        api.get('/transfers' + (user.role !== 'ADMIN' ? `?baseId=${user.baseId}` : '')),
        api.get('/equipment-types'),
        api.get('/bases')
      ]);
      setTransfers(transfersRes.data);
      setEquipmentTypes(equipmentRes.data);
      setBases(basesRes.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/transfers', {
        ...formData,
        quantity: parseInt(formData.quantity),
        fromBaseId: user.role !== 'ADMIN' ? user.baseId : parseInt(formData.fromBaseId),
        toBaseId: parseInt(formData.toBaseId)
      });
      setShowForm(false);
      fetchData();
    } catch (error) {
      console.error("Error creating transfer", error);
      alert(error.response?.data?.message || "Failed to create transfer");
    }
  };

  const updateStatus = async (id, action) => {
    try {
      await api.put(`/transfers/${id}/${action}`);
      fetchData();
    } catch (error) {
      alert("Failed to update transfer status");
    }
  };

  return (
    <div className="space-y-6 relative">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ArrowRightLeft className="mr-3 text-brand-teal" />
          Transfers
        </h1>
        <button 
          onClick={() => setShowForm(true)}
          className="bg-brand-teal text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center"
        >
          <Plus size={18} className="mr-2" /> Initiate Transfer
        </button>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h2 className="text-lg font-bold text-slate-700">Initiate Transfer</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-400 hover:text-slate-600"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Equipment</label>
                <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, equipmentTypeId: e.target.value})}>
                  <option value="">Select Equipment</option>
                  {equipmentTypes.map(eq => <option key={eq.id} value={eq.id}>{eq.equipmentName}</option>)}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Quantity</label>
                  <input required type="number" min="1" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, quantity: e.target.value})} />
                </div>
                {user.role === 'ADMIN' && (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">From Base</label>
                    <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, fromBaseId: e.target.value})}>
                      <option value="">Source Base</option>
                      {bases.map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                    </select>
                  </div>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">To Base</label>
                <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, toBaseId: e.target.value})}>
                  <option value="">Destination Base</option>
                  {bases.filter(b => b.id !== (user.baseId || formData.fromBaseId)).map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Remarks</label>
                <textarea className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, remarks: e.target.value})}></textarea>
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-slate-600 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-brand-teal text-white rounded-lg font-medium">Initiate Transfer</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Ref #</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Equipment</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Qty</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Route</th>
              <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase">Status</th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {transfers.map(t => (
              <tr key={t.id}>
                <td className="px-6 py-4 font-mono text-sm text-slate-500">{t.referenceNumber}</td>
                <td className="px-6 py-4 text-sm font-medium text-slate-800">{t.equipmentType.equipmentName}</td>
                <td className="px-6 py-4 text-sm font-bold text-slate-800">{t.quantity}</td>
                <td className="px-6 py-4 text-sm text-slate-600">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold">{t.fromBase.baseName}</span>
                    <ArrowRightLeft size={14} className="text-slate-400" />
                    <span className="font-semibold">{t.toBase.baseName}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-center">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                    t.status === 'PENDING' ? 'bg-yellow-100 text-yellow-700' :
                    t.status === 'APPROVED' ? 'bg-blue-100 text-blue-700' :
                    t.status === 'COMPLETED' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}>
                    {t.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-right space-x-2">
                  {t.status === 'PENDING' && (user.role === 'ADMIN' || user.baseId === t.toBase.id) && (
                    <button onClick={() => updateStatus(t.id, 'approve')} className="text-blue-600 hover:bg-blue-50 p-1.5 rounded" title="Approve">
                      <Check size={18} />
                    </button>
                  )}
                  {t.status === 'APPROVED' && (user.role === 'ADMIN' || user.baseId === t.toBase.id) && (
                    <button onClick={() => updateStatus(t.id, 'complete')} className="text-green-600 hover:bg-green-50 p-1.5 rounded" title="Mark Completed">
                      <PackageCheck size={18} />
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Transfers;
""",

    "Users.jsx": """import React, { useState, useEffect, useContext } from 'react';
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
      const [usersRes, basesRes] = await Promise.all([
        api.get('/users'),
        api.get('/bases')
      ]);
      setUsers(usersRes.data);
      setBases(basesRes.data);
    } catch (error) {
      console.error(error);
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
"""
}

for name, content in pages.items():
    with open(f"{frontend_src}/pages/{name}", "w", encoding="utf-8") as f:
        f.write(content)

print("Added functionality to React pages.")
