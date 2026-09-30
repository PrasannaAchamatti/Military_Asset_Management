import React, { useState, useEffect, useContext } from 'react';
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
    purchaseDate: new Date().toISOString().split('T')[0],
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
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Purchase Date</label>
                  <input required type="date" className="w-full border border-slate-300 rounded-lg p-2" value={formData.purchaseDate} onChange={e => setFormData({...formData, purchaseDate: e.target.value})} />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Equipment</label>
                  <select required className="w-full border border-slate-300 rounded-lg p-2" onChange={e => setFormData({...formData, equipmentTypeId: e.target.value})}>
                    <option value="">Select Equipment</option>
                    {equipmentTypes.map(eq => <option key={eq.id} value={eq.id}>{eq.equipmentName} ({eq.equipmentCode})</option>)}
                  </select>
                </div>
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
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Ref No.</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Remarks</th>
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
                <td className="px-6 py-4 text-sm text-slate-600">{p.referenceNumber}</td>
                <td className="px-6 py-4 text-sm text-slate-600 max-w-xs truncate" title={p.remarks}>{p.remarks}</td>
              </tr>
            ))}
            {purchases.length === 0 && (
              <tr><td colSpan="7" className="text-center py-8 text-slate-500">No purchases found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Purchases;
