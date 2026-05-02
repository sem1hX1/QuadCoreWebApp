import React, { useState, useEffect } from 'react';
import { Search, MoreHorizontal, ChevronRight, TrendingUp, TrendingDown, Package, Truck, AlertTriangle, PlayCircle, HelpCircle, ArrowRight } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import { searchComponents, analyzeComponent } from '../services/api';
import { useLocation, useNavigate } from 'react-router-dom';

const mockComponents = [
  { id: 1, name: 'ESP32-WROOM-32D', supplier: 'Digi-Key', supplierColor: '#e53935', price: 3.85, stock: 38, status: 'Stok', ai: 'Mouser ($1.75, Stok Teslim)', category: 'WiFi+BT MCU' },
  { id: 2, name: 'ESP32-WROOM-32U', supplier: 'AliExpress', supplierColor: '#ff6d00', price: 4.15, stock: '8Bin+', status: 'Özellikler', ai: 'AliExpress ($1.40, 15Bin+ Stok)', category: 'WiFi+BT MCU' },
  { id: 3, name: 'ESP32-WROOM-32', supplier: 'Digi-Key', supplierColor: '#e53935', price: 3.85, stock: 28, status: 'Özellikler', ai: 'Mouser ($1.75, Stok Teslim)', category: 'WiFi+BT MCU' },
  { id: 4, name: 'ESP-WROOM-02', supplier: 'AliExpress', supplierColor: '#ff6d00', price: 2.15, stock: '8Bin+', status: 'Özellikler', ai: 'AliExpress ($1.50, Stock Shipping)', category: 'WiFi MCU' },
  { id: 5, name: 'ESP32-S3-WROOM-1', supplier: 'Digi-Key', supplierColor: '#e53935', price: 4.25, stock: '2K', status: 'Özellikler', ai: 'LCSC ($1.90, Stock Shipping)', category: 'WiFi+BT MCU' },
  { id: 6, name: 'ESP32-C3-WROOM-02', supplier: 'Mouser', supplierColor: '#1e88e5', price: 1.75, stock: 24, status: 'Özellikler', ai: 'LCSC ($1.20, Stock Shipping)', category: 'RISC-V MCU' },
];

const trendData = [
  { month: 'Oca', fiyat: 4.2 }, { month: 'Şub', fiyat: 4.5 }, { month: 'Mar', fiyat: 3.9 },
  { month: 'Nis', fiyat: 3.8 }, { month: 'May', fiyat: 4.1 }, { month: 'Haz', fiyat: 3.85 },
];

const priceComparison = [
  { supplier: 'AliExpress', price: '$3.85', bold: true },
  { supplier: 'Digi-Key', price: '$4.20' },
  { supplier: 'Mouser', price: '$4.15' },
  { supplier: 'LCSC', price: '$3.95' },
];

const SupplierBadge = ({ name, color }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
    <div style={{ width: 14, height: 14, borderRadius: '3px', background: color, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <span style={{ fontSize: '0.55rem', color: '#fff', fontWeight: '800' }}>{name[0]}</span>
    </div>
    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '500' }}>{name}</span>
  </div>
);

const ComponentCard = ({ comp, index, isSelected, onClick }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: index * 0.05 }}
    onClick={onClick}
    style={{
      background: isSelected ? 'var(--bg-sidebar)' : 'var(--bg-card)',
      border: `1px solid ${isSelected ? 'var(--accent)' : 'var(--border)'}`,
      boxShadow: isSelected ? '0 0 0 1px var(--accent), 0 4px 6px -1px rgba(0, 0, 0, 0.05)' : '0 1px 3px rgba(0,0,0,0.05)',
      borderRadius: '10px',
      padding: '14px',
      cursor: 'pointer',
      transition: 'all 0.15s',
      position: 'relative',
    }}
    className="comp-card"
  >
    <div style={{ position: 'absolute', top: 10, left: 14, width: 18, height: 18, borderRadius: '4px', background: 'var(--bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.65rem', fontWeight: '700', color: 'var(--text-muted)' }}>
      {comp.id}
    </div>
    <button style={{ position: 'absolute', top: 8, right: 8, background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', padding: '2px' }}>
      <MoreHorizontal size={14} />
    </button>

    <div style={{ display: 'flex', gap: '10px', marginTop: '4px' }}>
      <div style={{ width: 48, height: 48, borderRadius: '6px', background: 'var(--bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Package size={20} color="var(--text-dim)" />
      </div>

      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '4px', paddingLeft: '22px' }}>
          <span style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--text-main)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{comp.name}</span>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginLeft: '8px', flexShrink: 0, marginRight: '18px' }}>{comp.status}</span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <SupplierBadge name={comp.supplier} color={comp.supplierColor} />
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)' }}>${comp.price.toFixed(2)}</div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{comp.stock} Stok</div>
          </div>
        </div>

        <div style={{
          background: 'rgba(2, 132, 199, 0.08)',
          border: '1px solid rgba(2, 132, 199, 0.15)',
          borderRadius: '5px',
          padding: '5px 8px',
          fontSize: '0.72rem',
          color: 'var(--accent)',
          lineHeight: '1.3',
        }}>
          ✦ Yapay Zeka En İyi Eşleşme: {comp.ai}
        </div>
      </div>
    </div>
  </motion.div>
);

const DetailPanel = ({ comp }) => (
  <div style={{
    width: '300px',
    minWidth: '300px',
    background: 'var(--bg-sidebar)',
    borderLeft: '1px solid var(--border)',
    height: 'calc(100vh - 52px)',
    overflowY: 'auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    boxShadow: '-4px 0 15px rgba(0,0,0,0.02)'
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <h3 style={{ fontSize: '1rem', fontWeight: '600', color: 'var(--text-main)' }}>Bileşen Detayı</h3>
      <button style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
        <MoreHorizontal size={18} />
      </button>
    </div>

    <div style={{ background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '8px', padding: '12px', display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
      <div style={{ width: 10, height: 10, borderRadius: '2px', background: 'var(--accent)', marginTop: '4px', flexShrink: 0 }} />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--text-main)', marginBottom: '4px' }}>{comp.name}</div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px', lineHeight: '1.4' }}>Kategori: {comp.category}<br/>Paket: SMD/QFN-32<br/>Çalışma Voltajı: 3.0V - 3.6V</div>
        <div style={{ background: 'rgba(2, 132, 199, 0.08)', borderRadius: '4px', padding: '6px 8px', fontSize: '0.75rem', color: 'var(--accent)', lineHeight: '1.4', border: '1px solid rgba(2, 132, 199, 0.1)' }}>
          ✦ Yapay Zeka Önerisi: En uygun fiyat ve lojistik kombinasyonu AliExpress'te tespit edildi. (Güvenilirlik: %94)
        </div>
      </div>
    </div>

    <div>
      <h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600', letterSpacing: '0.5px', marginBottom: '12px', textTransform: 'uppercase' }}>Fiyat Karşılaştırması</h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', background: 'var(--bg)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border)' }}>
        {priceComparison.map((item, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: i !== priceComparison.length - 1 ? '8px' : '0', borderBottom: i !== priceComparison.length - 1 ? '1px solid var(--border)' : 'none' }}>
            <span style={{ fontSize: '0.85rem', color: item.bold ? 'var(--text-main)' : 'var(--text-muted)', fontWeight: item.bold ? '600' : '500' }}>{item.supplier}</span>
            <span style={{ fontSize: '0.85rem', color: item.bold ? 'var(--accent)' : 'var(--text-main)', fontWeight: item.bold ? '700' : '600' }}>{item.price}</span>
          </div>
        ))}
      </div>
    </div>

    <div>
      <h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600', letterSpacing: '0.5px', marginBottom: '12px', textTransform: 'uppercase' }}>Fiyat Trendi (6 Ay)</h4>
      <div style={{ height: '140px', background: 'var(--bg)', padding: '10px 10px 10px 0', borderRadius: '8px', border: '1px solid var(--border)' }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trendData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="detailGradLight" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--accent)" stopOpacity={0.15} />
                <stop offset="95%" stopColor="var(--accent)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
            <XAxis dataKey="month" tick={{ fontSize: 10, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} />
            <YAxis domain={['auto', 'auto']} tick={{ fontSize: 10, fill: 'var(--text-muted)' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ background: '#fff', border: '1px solid var(--border)', borderRadius: '6px', fontSize: '0.8rem', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }} />
            <Area type="monotone" dataKey="fiyat" stroke="var(--accent)" strokeWidth={2} fill="url(#detailGradLight)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: 'auto', paddingTop: '20px' }}>
      {[
        { label: 'Aktif Tedarikçiler', value: '24 Tedarikçi', icon: <Package size={14} /> },
        { label: 'Tahmini Teslimat', value: '4-7 İş Günü', icon: <Truck size={14} /> },
        { label: 'Risk Uyarıları', value: 'Düşük Risk', icon: <AlertTriangle size={14} />, color: '#10b981' },
      ].map((stat, i) => (
        <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 12px', background: 'var(--bg)', borderRadius: '6px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            <span style={{ color: stat.color || 'var(--text-dim)' }}>{stat.icon}</span>
            {stat.label}
          </div>
          <span style={{ fontSize: '0.85rem', fontWeight: '600', color: stat.color || 'var(--text-main)' }}>{stat.value}</span>
        </div>
      ))}
      <button className="premium-button" style={{ marginTop: '10px', width: '100%', padding: '12px' }}>
        Satın Alma Seçeneklerini Gör
      </button>
    </div>
  </div>
);

const LandingView = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '60px 20px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ fontSize: '3rem', fontWeight: '800', color: 'var(--text-main)', marginBottom: '16px' }}>Akıllı Komponent Analizi</h1>
        <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', lineHeight: '1.6', maxWidth: '600px', margin: '0 auto' }}>
          Dünya çapındaki distribütörleri saniyeler içinde tarayın. En uygun fiyatı, stok durumunu ve lojistik rotasını yapay zeka ile keşfedin.
        </p>
      </motion.div>

      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} style={{ width: '100%', marginBottom: '80px' }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          background: 'var(--bg-card)',
          border: '1px solid var(--border)',
          boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)',
          borderRadius: '12px', padding: '12px 20px',
        }}>
          <Search size={22} color="var(--text-dim)" />
          <input
            type="text"
            placeholder="Parça numarası, üretici veya özellik girin (Örn: ESP32-WROOM)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
            style={{
              background: 'none', border: 'none', outline: 'none',
              color: 'var(--text-main)', fontSize: '1.1rem', flex: 1,
              fontFamily: 'Inter, sans-serif', padding: '8px 0'
            }}
          />
          <button
            onClick={() => onSearch(query)}
            className="premium-button"
            style={{ padding: '10px 24px', fontSize: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            Ara <ArrowRight size={18} />
          </button>
        </div>
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginRight: '5px' }}>Önerilenler:</span>
          {['STM32F103', 'ESP32', 'LM317', 'ATMEGA328P'].map(tag => (
            <span key={tag} onClick={() => onSearch(tag)} style={{ fontSize: '0.85rem', color: 'var(--accent)', cursor: 'pointer', background: 'rgba(2, 132, 199, 0.08)', padding: '2px 10px', borderRadius: '12px' }}>
              {tag}
            </span>
          ))}
        </div>
      </motion.div>

      {/* Info Sections */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '60px' }}>
        
        {/* Nasıl Çalışır? */}
        <section>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '25px', justifyContent: 'center' }}>
            <PlayCircle size={24} color="var(--accent)" />
            <h2 style={{ fontSize: '1.8rem', color: 'var(--text-main)', fontWeight: '700' }}>Sistem Nasıl Çalışır?</h2>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
            {[
              { title: '1. Tarama', desc: 'Mouser, DigiKey, LCSC gibi 50+ küresel distribütör eş zamanlı olarak taranır.' },
              { title: '2. Yapay Zeka Analizi', desc: 'Gümrük, kargo süreleri ve fiyat avantajları yapay zeka tarafından hesaplanır.' },
              { title: '3. Optimizasyon', desc: 'Size en ucuz değil, en optimum (hız + maliyet) satın alma rotası sunulur.' }
            ].map((step, i) => (
              <div key={i} className="glass-card" style={{ padding: '24px', textAlign: 'center' }}>
                <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 15px auto', fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--accent)' }}>{i + 1}</div>
                <h4 style={{ fontSize: '1.1rem', marginBottom: '10px', color: 'var(--text-main)' }}>{step.title}</h4>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.5' }}>{step.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Sıkça Sorulan Sorular */}
        <section>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '25px', justifyContent: 'center' }}>
            <HelpCircle size={24} color="var(--accent)" />
            <h2 style={{ fontSize: '1.8rem', color: 'var(--text-main)', fontWeight: '700' }}>Sıkça Sorulan Sorular</h2>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {[
              { q: 'Hangi tedarikçileri destekliyorsunuz?', a: 'Mouser, DigiKey, Farnell, Arrow, AliExpress ve LCSC dahil olmak üzere 50\'den fazla global distribütörü canlı destekliyoruz.' },
              { q: 'Fiyatlara gümrük vergileri dahil mi?', a: 'Yapay zeka analiz raporlarında, ülkenize özgü tahmini gümrük vergileri ve kargo masrafları hesaplamalara dahil edilmektedir.' },
              { q: 'Veriler ne sıklıkla güncelleniyor?', a: 'Tüm stok ve fiyat verileri anlık olarak API üzerinden çekilir, önbellek süresi maksimum 5 dakikadır.' }
            ].map((faq, i) => (
              <div key={i} className="glass-card" style={{ padding: '20px 24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <h4 style={{ fontSize: '1.05rem', color: 'var(--text-main)', fontWeight: '600' }}>{faq.q}</h4>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: '1.5' }}>{faq.a}</p>
              </div>
            ))}
          </div>
        </section>

      </motion.div>
    </div>
  );
}

const Dashboard = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedComp, setSelectedComp] = useState(mockComponents[0]);
  const [results, setResults] = useState(mockComponents);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Check if there is a search query in the URL params
    const params = new URLSearchParams(location.search);
    const q = params.get('q');
    if (q) {
      performSearch(q);
    } else {
      // Ana Sayfa linkine tıklandığında (veya URL'de q parametresi yoksa) aramayı sıfırla
      setHasSearched(false);
      setSearchQuery('');
    }
  }, [location.search]);

  const handleSearch = (queryToSearch) => {
    const q = typeof queryToSearch === 'string' ? queryToSearch : searchQuery;
    if (!q.trim()) return;
    
    // Update the URL which will trigger the useEffect
    navigate(`/?q=${encodeURIComponent(q)}`);
  };

  const performSearch = async (q) => {
    setSearchQuery(q);
    setLoading(true);
    setHasSearched(true);
    
    try {
      const data = await searchComponents(q);
      const newResults = data.length > 0 ? data : mockComponents;
      setResults(newResults);
      setSelectedComp(newResults[0]);
    } catch {
      setResults(mockComponents);
      setSelectedComp(mockComponents[0]);
    } finally {
      setLoading(false);
    }
  };

  if (!hasSearched) {
    return <LandingView onSearch={handleSearch} />;
  }

  return (
    <div style={{ display: 'flex', height: 'calc(100vh - 52px)', overflow: 'hidden' }}>
      {/* Center Content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '24px 30px', background: 'var(--bg)' }}>
        
        {/* Search Bar (Top) */}
        <div style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: '700', color: 'var(--text-main)' }}>Arama Sonuçları</h2>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: '8px', padding: '8px 16px',
            width: '400px', boxShadow: '0 2px 4px rgba(0,0,0,0.02)'
          }}>
            <Search size={16} color="var(--text-dim)" />
            <input
              type="text"
              placeholder="Bileşen veya parça numarası ara..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              style={{
                background: 'none', border: 'none', outline: 'none',
                color: 'var(--text-main)', fontSize: '0.95rem', flex: 1,
                fontFamily: 'Inter, sans-serif',
              }}
            />
            <button
              onClick={() => handleSearch()}
              style={{
                background: 'var(--bg)', border: '1px solid var(--border)',
                borderRadius: '5px', padding: '4px 12px', color: 'var(--text-main)',
                fontSize: '0.85rem', cursor: 'pointer', fontFamily: 'Inter, sans-serif',
                transition: 'all 0.15s', fontWeight: '500'
              }}
              className="search-btn-mini"
            >
              {loading ? '...' : 'Ara'}
            </button>
          </div>
        </div>

        {/* Component Grid - 2 columns */}
        {loading ? (
           <div style={{ display: 'flex', justifyContent: 'center', padding: '100px' }}>
              <div style={{ border: '3px solid var(--border)', borderTopColor: 'var(--accent)', borderRadius: '50%', width: 40, height: 40, animation: 'spin 1s linear infinite' }} />
           </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '16px', marginBottom: '30px' }}>
            {results.map((comp, i) => (
              <ComponentCard
                key={comp.id}
                comp={comp}
                index={i}
                isSelected={selectedComp?.id === comp.id}
                onClick={() => setSelectedComp(comp)}
              />
            ))}
          </div>
        )}

      </div>

      {/* Right Detail Panel */}
      {selectedComp && !loading && <DetailPanel comp={selectedComp} />}

      <style>{`
        .comp-card:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
          border-color: var(--accent) !important;
          transform: translateY(-2px);
        }
        .search-btn-mini:hover {
          background: var(--border) !important;
        }
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};

export default Dashboard;
