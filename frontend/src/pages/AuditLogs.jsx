import React, { useState, useEffect } from 'react';
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
