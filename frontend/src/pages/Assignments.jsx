import React, { useState, useEffect, useContext } from 'react';
import api from '../api/axios';
import { ClipboardCheck, Plus, X } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Assignments = () => {
  const { user } = useContext(AuthContext);
  const [assignments, setAssignments] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [bases, setBases] = useState([]);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    equipmentTypeId: '',
    quantity: '',
    baseId: '',
    personnelName: '',
    personnelId: '',
    assignedDate: new Date().toISOString().split('T')[0],
    remarks: ''
  });

  const fetchData = async () => {
    try {
      const baseQuery = user.role !== 'ADMIN' ? `?baseId=${user.baseId}` : '';
      const [assignmentsRes, inventoryRes, basesRes] = await Promise.all([
        api.get('/assignments' + baseQuery),
        api.get('/inventory' + baseQuery),
        api.get('/bases')
      ]);
      setAssignments(assignmentsRes.data);
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
      await api.post('/assignments', {
        ...formData,
        quantity: parseInt(formData.quantity),
        baseId: user.role !== 'ADMIN' ? user.baseId : parseInt(formData.baseId)
      });
      setShowForm(false);
      fetchData();
    } catch (error) {
      console.error("Error creating assignment", error);
      alert(error.response?.data?.message || "Failed to create assignment");
    }
  };

  const targetBaseId = user.role !== 'ADMIN' ? user.baseId : parseInt(formData.baseId);
  const availableEquipment = inventory.filter(inv => inv.base.id === targetBaseId && inv.quantity > 0);
  const selectedInventory = availableEquipment.find(inv => inv.equipmentType.id === parseInt(formData.equipmentTypeId));
  const maxQuantity = selectedInventory ? selectedInventory.quantity : undefined;

  return (
    <div className="space-y-6 relative">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ClipboardCheck className="mr-3 text-orange-500" />
          Assignments
        </h1>
        <button 
          onClick={() => setShowForm(true)}
          className="bg-orange-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-orange-600 transition-colors flex items-center"
        >
          <Plus size={18} className="mr-2" /> Assign Equipment
        </button>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
              <h2 className="text-lg font-bold text-slate-700">Assign Equipment</h2>
              <button onClick={() => setShowForm(false)} className="text-slate-400 hover:text-slate-600"><X size={20}/></button>
            </div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              {user.role === 'ADMIN' && (
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Base</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" value={formData.baseId} onChange={e => setFormData({...formData, baseId: e.target.value, equipmentTypeId: ''})}>
                    <option value="">Select Base</option>
                    {bases.map(b => <option key={b.id} value={b.id}>{b.baseName}</option>)}
                  </select>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Equipment</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" value={formData.equipmentTypeId} onChange={e => setFormData({...formData, equipmentTypeId: e.target.value})} disabled={user.role === 'ADMIN' && !formData.baseId}>
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
                  <label className="block text-sm font-medium text-slate-700 mb-1">Personnel Name</label>
                  <input required type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, personnelName: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Personnel ID</label>
                  <input required type="text" className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, personnelId: e.target.value})} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Assigned Date</label>
                  <input type="date" required value={formData.assignedDate} className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, assignedDate: e.target.value})} />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Remarks</label>
                <textarea className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, remarks: e.target.value})}></textarea>
              </div>
              <div className="pt-4 flex justify-end space-x-3">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-slate-600 font-medium">Cancel</button>
                <button type="submit" className="px-4 py-2 bg-orange-500 text-white rounded-lg font-medium">Assign</button>
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
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Personnel Name</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Personnel ID</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {assignments.map(a => (
              <tr key={a.id}>
                <td className="px-6 py-4 text-sm text-slate-600">{a.assignedDate}</td>
                <td className="px-6 py-4 text-sm font-medium text-slate-800">{a.equipmentType?.equipmentName}</td>
                <td className="px-6 py-4 text-sm font-bold text-slate-800">{a.quantity}</td>
                <td className="px-6 py-4 text-sm text-slate-600 font-semibold">{a.personnelName}</td>
                <td className="px-6 py-4 text-sm text-slate-500">{a.personnelId}</td>
              </tr>
            ))}
            {assignments.length === 0 && (
              <tr><td colSpan="5" className="text-center py-8 text-slate-500">No assignments found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Assignments;
