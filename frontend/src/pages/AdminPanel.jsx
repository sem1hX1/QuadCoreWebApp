import React from 'react';
import { Save, Globe, Key, Bell } from 'lucide-react';

const AdminPanel = () => {
  return (
    <div className="animate-fade-in">
      <h2 style={{ fontSize: '2rem', marginBottom: '30px' }}>Yönetim Paneli</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '30px' }}>
        {/* Sidebar Settings */}
        <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ padding: '10px', background: 'var(--primary)', borderRadius: '8px', cursor: 'pointer' }}>Genel Ayarlar</div>
          <div style={{ padding: '10px', cursor: 'pointer', color: 'var(--text-muted)' }}>API Entegrasyonları</div>
          <div style={{ padding: '10px', cursor: 'pointer', color: 'var(--text-muted)' }}>Tedarikçi Listesi</div>
        </div>

        {/* Content Settings */}
        <div className="glass-card" style={{ padding: '30px' }}>
          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'block', marginBottom: '10px', fontWeight: '500' }}>Site Başlığı</label>
            <input type="text" className="input-glass" style={{ width: '100%' }} defaultValue="ComponentSource AI" />
          </div>

          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'block', marginBottom: '10px', fontWeight: '500' }}>Desteklenen Siteler</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {['Mouser', 'DigiKey', 'Farnell', 'Arrow', 'LCSC'].map(site => (
                <span key={site} style={{ padding: '5px 12px', background: 'rgba(255,255,255,0.1)', borderRadius: '20px', fontSize: '0.8rem' }}>
                  {site}
                </span>
              ))}
            </div>
          </div>

          <div style={{ marginBottom: '30px' }}>
            <label style={{ display: 'block', marginBottom: '10px', fontWeight: '500' }}>AI Analiz Derinliği</label>
            <select className="input-glass" style={{ width: '100%' }}>
              <option>Hızlı (Sadece Fiyat)</option>
              <option selected>Dengeli (Fiyat + Kargo)</option>
              <option>Derin (Tüm Parametreler)</option>
            </select>
          </div>

          <button className="premium-button" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Save size={20} />
            Değişiklikleri Kaydet
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
