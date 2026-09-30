import os

frontend_src = "f:/Military_Manage/frontend/src"

pages = {
    "Purchases.jsx": """import React from 'react';
import { ShoppingCart } from 'lucide-react';

const Purchases = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ShoppingCart className="mr-3 text-brand-blue" />
          Purchases
        </h1>
        <button className="bg-brand-blue text-white px-4 py-2 rounded-lg font-medium hover:bg-brand-accent transition-colors">
          + New Purchase
        </button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center text-slate-500">
        Purchases module coming soon. (This is a simplified scaffold for demonstration)
      </div>
    </div>
  );
};

export default Purchases;
""",
    "Transfers.jsx": """import React from 'react';
import { ArrowRightLeft } from 'lucide-react';

const Transfers = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ArrowRightLeft className="mr-3 text-brand-teal" />
          Transfers
        </h1>
        <button className="bg-brand-teal text-white px-4 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity">
          + Initiate Transfer
        </button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center text-slate-500">
        Transfers module coming soon.
      </div>
    </div>
  );
};

export default Transfers;
""",
    "Assignments.jsx": """import React from 'react';
import { ClipboardCheck } from 'lucide-react';

const Assignments = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <ClipboardCheck className="mr-3 text-orange-500" />
          Assignments & Expenditures
        </h1>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center text-slate-500">
        Assignments module coming soon.
      </div>
    </div>
  );
};

export default Assignments;
""",
    "Users.jsx": """import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { Users as UsersIcon } from 'lucide-react';

const Users = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get('/users').then(res => setUsers(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <UsersIcon className="mr-3 text-brand-navy" />
          User Management
        </h1>
        <button className="bg-brand-navy text-white px-4 py-2 rounded-lg font-medium hover:bg-slate-800 transition-colors">
          + Add User
        </button>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Name</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Username</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Role</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {users.map(u => (
              <tr key={u.id}>
                <td className="px-6 py-4">{u.fullName}</td>
                <td className="px-6 py-4 font-mono text-slate-500">{u.username}</td>
                <td className="px-6 py-4">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">{u.role}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;
""",
    "AuditLogs.jsx": """import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { Activity } from 'lucide-react';

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    api.get('/audit-logs').then(res => setLogs(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Activity className="mr-3 text-brand-navy" />
        <h1 className="text-2xl font-bold text-slate-800">System Audit Logs</h1>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full whitespace-nowrap">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Time</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">User</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Action</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Entity</th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Description</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm text-slate-700">
            {logs.map(log => (
              <tr key={log.id} className="hover:bg-slate-50">
                <td className="px-6 py-4">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="px-6 py-4">{log.username}</td>
                <td className="px-6 py-4 font-mono text-xs">{log.action}</td>
                <td className="px-6 py-4">{log.entityType} #{log.entityId}</td>
                <td className="px-6 py-4">{log.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AuditLogs;
"""
}

for name, content in pages.items():
    with open(f"{frontend_src}/pages/{name}", "w", encoding="utf-8") as f:
        f.write(content)

print("Remaining pages scaffolded.")
