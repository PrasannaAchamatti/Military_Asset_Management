import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import { ArrowRightLeft, Plus, X, Check, PackageCheck } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Transfers = () => {
  const { user } = useContext(AuthContext);
  const [transfers, setTransfers] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [bases, setBases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    equipmentTypeId: '',
    quantity: '',
    fromBaseId: '',
    toBaseId: '',
    transferDate: new Date().toISOString().split('T')[0],
    remarks: ''
  });

  const fetchData = async () => {
    try {
      const baseQuery = user.role !== 'ADMIN' ? `?baseId=${user.baseId}` : '';
      const [transfersRes, inventoryRes, basesRes] = await Promise.all([
        api.get('/transfers' + baseQuery),
        api.get('/inventory' + baseQuery),
        api.get('/bases')
      ]);
      setTransfers(transfersRes.data);
      setInventory(inventoryRes.data);
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

  const targetBaseId = user.role !== 'ADMIN' ? user.baseId : parseInt(formData.fromBaseId);
  const availableEquipment = inventory.filter(inv => inv.base.id === targetBaseId && inv.quantity > 0);
  const selectedInventory = availableEquipment.find(inv => inv.equipmentType.id === parseInt(formData.equipmentTypeId));
  const maxQuantity = selectedInventory ? selectedInventory.quantity : undefined;

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
              {user.role === 'ADMIN' && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">From Base</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" value={formData.fromBaseId} onChange={e => setFormData({...formData, fromBaseId: e.target.value, equipmentTypeId: ''})}>
                    <option value="">Source Base</option>
                    {bases.map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                  </select>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Equipment</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" value={formData.equipmentTypeId} onChange={e => setFormData({...formData, equipmentTypeId: e.target.value})} disabled={user.role === 'ADMIN' && !formData.fromBaseId}>
                    <option value="">Select Equipment</option>
                    {availableEquipment.map(inv => (
                      <option key={inv.equipmentType.id} value={inv.equipmentType.id}>
                        {inv.equipmentType.equipmentName} (Avail: {inv.quantity})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Quantity</label>
                  <input required type="number" min="1" max={maxQuantity || ''} value={formData.quantity} className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, quantity: e.target.value})} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">To Base</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" value={formData.toBaseId} onChange={e => setFormData({...formData, toBaseId: e.target.value})}>
                    <option value="">Destination Base</option>
                    {bases.filter(b => b.id !== (user.role !== 'ADMIN' ? user.baseId : parseInt(formData.fromBaseId))).map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Transfer Date</label>
                  <input type="date" required value={formData.transferDate} className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, transferDate: e.target.value})} />
                </div>
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
