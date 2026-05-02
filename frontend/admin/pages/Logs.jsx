import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Terminal, RefreshCw, AlertCircle, Info, ShieldAlert, Search, Trash2 } from 'lucide-react';
import axios from 'axios';

const LogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLevel, setFilterLevel] = useState('ALL');

  const fetchLogs = async () => {
    setLoading(true);
    try {
      // Backend admin/logs uç noktasından verileri çek
      const response = await axios.get('http://localhost:8000/admin/logs');
      setLogs(response.data);
    } catch (error) {
      console.error('Loglar çekilirken hata oluştu:', error);
      // Hata durumunda boş liste veya demo verisi gösterilebilir
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLevel = filterLevel === 'ALL' || log.level === filterLevel;
    return matchesSearch && matchesLevel;
  });

  const getLevelColor = (level) => {
    switch (level) {
      case 'ERROR': return '#ef4444';
      case 'WARNING': return '#f59e0b';
      case 'INFO': return '#3b82f6';
      default: return '#64748b';
    }
  };

  const getLevelIcon = (level) => {
    switch (level) {
      case 'ERROR': return <ShieldAlert size={14} color="#ef4444" />;
      case 'WARNING': return <AlertCircle size={14} color="#f59e0b" />;
      case 'INFO': return <Info size={14} color="#3b82f6" />;
      default: return <Terminal size={14} color="#64748b" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ padding: '24px' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1e293b', marginBottom: '4px' }}>Sistem Logları</h2>
          <p style={{ color: '#64748b', fontSize: '0.9rem' }}>Sistemin arka planındaki olayları ve hataları takip edin.</p>
        </div>
        <button 
          onClick={fetchLogs}
          disabled={loading}
          style={{ 
            display: 'flex', alignItems: 'center', gap: '8px', 
            padding: '8px 16px', borderRadius: '8px', background: '#0284c7', 
            color: '#fff', border: 'none', cursor: 'pointer', fontSize: '0.9rem' 
          }}
        >
          <RefreshCw size={16} className={loading ? 'spin' : ''} />
          {loading ? 'Yükleniyor...' : 'Yenile'}
        </button>
      </div>

      <div style={{ 
        background: '#fff', borderRadius: '12px', border: '1px solid #e2e8f0', 
        padding: '16px', marginBottom: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap' 
      }}>
        <div style={{ flex: 1, position: 'relative', minWidth: '200px' }}>
          <Search size={18} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input 
            type="text" 
            placeholder="Loglarda ara..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ 
              width: '100%', padding: '10px 12px 10px 40px', borderRadius: '8px', 
              border: '1px solid #e2e8f0', outline: 'none', fontSize: '0.9rem' 
            }}
          />
        </div>
        <select 
          value={filterLevel}
          onChange={(e) => setFilterLevel(e.target.value)}
          style={{ 
            padding: '10px 16px', borderRadius: '8px', border: '1px solid #e2e8f0', 
            background: '#fff', outline: 'none', fontSize: '0.9rem', minWidth: '150px' 
          }}
        >
          <option value="ALL">Tüm Seviyeler</option>
          <option value="INFO">Bilgi (INFO)</option>
          <option value="WARNING">Uyarı (WARNING)</option>
          <option value="ERROR">Hata (ERROR)</option>
        </select>
      </div>

      <div style={{ 
        background: '#0f172a', borderRadius: '12px', overflow: 'hidden', 
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)' 
      }}>
        <div style={{ 
          maxHeight: '600px', overflowY: 'auto', padding: '16px', 
          fontFamily: 'JetBrains Mono, Courier New, monospace', fontSize: '0.85rem' 
        }}>
          {filteredLogs.length > 0 ? (
            filteredLogs.map((log, index) => (
              <div key={log.id || index} style={{ 
                display: 'flex', gap: '12px', padding: '8px 0', 
                borderBottom: '1px solid #1e293b', opacity: 0.9 
              }}>
                <span style={{ color: '#64748b', minWidth: '150px' }}>[{new Date(log.timestamp).toLocaleString()}]</span>
                <span style={{ 
                  color: getLevelColor(log.level), fontWeight: 'bold', 
                  minWidth: '80px', display: 'flex', alignItems: 'center', gap: '4px' 
                }}>
                  {getLevelIcon(log.level)} {log.level}
                </span>
                <span style={{ color: '#e2e8f0', flex: 1, wordBreak: 'break-all' }}>{log.message}</span>
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
              {loading ? 'Loglar yükleniyor...' : 'Eşleşen log bulunamadı.'}
            </div>
          )}
        </div>
      </div>

      <style>{`
        .spin { animation: spin 1s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </motion.div>
  );
};

export default LogsPage;
