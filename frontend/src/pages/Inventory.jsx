import React, { useState, useEffect } from 'react';
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
