import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Settings, Cpu, Search, History, Plus, MessageSquare, Menu, X, Clock } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import Iletisim from './pages/Iletisim';

const historyItems = [
  { id: 1, label: 'ESP32' },
  { id: 2, label: 'STM32F103' },
  { id: 3, label: 'LCSC' },
  { id: 4, label: 'Dirençler' },
  { id: 5, label: 'LED Sürücü' },
];

function Sidebar({ isOpen, setIsOpen }) {
  if (!isOpen) return null;

  return (
    <aside style={{
      width: '200px',
      minWidth: '200px',
      background: 'var(--bg-sidebar)',
      borderRight: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 50,
      boxShadow: '0 0 10px rgba(0,0,0,0.02)'
    }}>
      {/* Logo at top */}
      <div style={{ padding: '18px 16px 10px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '8px', textDecoration: 'none', color: 'inherit' }}>
          <div style={{ width: 28, height: 28, borderRadius: '6px', background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Cpu size={16} color="#fff" />
          </div>
          <span style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)', letterSpacing: '0.5px' }}>
            Source<span style={{ color: 'var(--text-main)', fontWeight: '400' }}>Flow</span>
          </span>
        </Link>
        <button onClick={() => setIsOpen(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '2px' }}>
          <X size={18} />
        </button>
      </div>

      {/* Search History */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 8px' }}>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.72rem', fontWeight: '600', letterSpacing: '1px', padding: '0 8px', marginBottom: '10px', textTransform: 'uppercase' }}>
          Arama Geçmişi
        </p>
        {historyItems.map(item => (
          <Link
            key={item.id}
            to={`/?q=${item.label}`}
            className="sidebar-history-item"
            style={{
              display: 'flex', alignItems: 'center', gap: '10px',
              padding: '9px 10px', borderRadius: '6px', cursor: 'pointer',
              color: 'var(--text-muted)', fontSize: '0.88rem', transition: 'all 0.15s', textDecoration: 'none'
            }}
          >
            <Clock size={13} color="var(--text-dim)" />
            <span>{item.label}</span>
          </Link>
        ))}
      </div>

      {/* Bottom Logo */}
      <div style={{ padding: '14px 16px', borderTop: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <div style={{ width: 22, height: 22, borderRadius: '4px', background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Cpu size={12} color="#fff" />
        </div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>SourceFlow AI</span>
      </div>
    </aside>
  );
}

function TopNav({ isSidebarOpen, setIsSidebarOpen }) {
  const location = useLocation();
  const navLinks = [
    { to: '/', label: 'Ana Sayfa' },
    { to: '/about', label: 'Hakkımızda' },
    { to: '/iletisim', label: 'İletişim' }
  ];

  return (
    <nav style={{
      position: 'fixed', top: 0, left: isSidebarOpen ? '200px' : '0', right: 0,
      height: '52px', zIndex: 40,
      background: 'rgba(255,255,255,0.85)',
      borderBottom: '1px solid var(--border)',
      backdropFilter: 'blur(12px)',
      display: 'flex', alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 28px',
      transition: 'left 0.2s ease'
    }}>
      {/* Left side: Hamburger if sidebar is closed */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
        {!isSidebarOpen && (
          <button onClick={() => setIsSidebarOpen(true)} style={{ background: 'none', border: 'none', color: 'var(--text-main)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
            <Menu size={20} />
          </button>
        )}
        {!isSidebarOpen && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-main)', fontWeight: '700' }}>
            <Cpu size={18} color="var(--accent)" /> SourceFlow
          </div>
        )}
      </div>

      {/* Nav Links - centered */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1, justifyContent: 'center' }}>
        {navLinks.map(link => {
          const isActive = location.pathname === link.to;
          return (
            <Link
              key={link.to}
              to={link.to}
              style={{
                padding: '6px 14px',
                borderRadius: '6px',
                textDecoration: 'none',
                fontSize: '0.88rem',
                fontWeight: '500',
                color: isActive ? 'var(--accent)' : 'var(--text-muted)',
                background: isActive ? 'rgba(2, 132, 199, 0.1)' : 'transparent',
                transition: 'all 0.15s',
              }}
              className="top-nav-link"
            >
              {link.label}
            </Link>
          );
        })}
      </div>

      {/* Right - Admin Link only (User login removed) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <a href="/admin/" style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          color: 'var(--text-muted)', textDecoration: 'none', fontSize: '0.85rem',
          padding: '6px 14px', borderRadius: '5px',
          background: 'var(--bg)', border: '1px solid var(--border)',
          transition: 'all 0.15s', fontWeight: '500'
        }} className="admin-link">
          <Settings size={14} />
          Admin Paneli
        </a>
      </div>
    </nav>
  );
}

function Footer() {
  return (
    <footer style={{
      background: 'var(--bg-sidebar)',
      borderTop: '1px solid var(--border)',
      padding: '40px 0',
      marginTop: 'auto',
      width: '100%'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '30px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '300px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-main)', fontWeight: '700', fontSize: '1.2rem' }}>
            <Cpu size={20} color="var(--accent)" /> SourceFlow AI
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', lineHeight: '1.6' }}>
            Akıllı tedarik zinciri optimizasyonu ile donanım üretim süreçlerinizi hızlandırın. En iyi parçaları en uygun fiyata bulun.
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '50px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <h4 style={{ color: 'var(--text-main)', fontSize: '0.9rem', fontWeight: '600' }}>Platform</h4>
            <Link to="/" style={{ color: 'var(--text-muted)', textDecoration: 'none', fontSize: '0.85rem' }}>Arama Motoru</Link>
            <Link to="/about" style={{ color: 'var(--text-muted)', textDecoration: 'none', fontSize: '0.85rem' }}>Hakkımızda</Link>
            <Link to="/iletisim" style={{ color: 'var(--text-muted)', textDecoration: 'none', fontSize: '0.85rem' }}>İletişim</Link>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <h4 style={{ color: 'var(--text-main)', fontSize: '0.9rem', fontWeight: '600' }}>Yasal</h4>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', cursor: 'pointer' }}>Gizlilik Politikası</span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', cursor: 'pointer' }}>Kullanım Şartları</span>
          </div>
        </div>
      </div>
      <div style={{ textAlign: 'center', marginTop: '30px', paddingTop: '20px', borderTop: '1px solid var(--border)', color: 'var(--text-dim)', fontSize: '0.8rem' }}>
        &copy; {new Date().getFullYear()} SourceFlow AI. Tüm hakları saklıdır.
      </div>
    </footer>
  );
}

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <Router>
      <div style={{ background: 'var(--bg)', minHeight: '100vh', color: 'var(--text-main)', display: 'flex' }}>
        <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />
        
        {/* Main Wrapper */}
        <div style={{ 
          flex: 1, 
          marginLeft: isSidebarOpen ? '200px' : '0', 
          transition: 'margin-left 0.2s ease',
          display: 'flex',
          flexDirection: 'column',
          minHeight: '100vh'
        }}>
          <TopNav isSidebarOpen={isSidebarOpen} setIsSidebarOpen={setIsSidebarOpen} />
          
          {/* Page content offset for navbar */}
          <div style={{ paddingTop: '52px', flex: 1, display: 'flex', flexDirection: 'column' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/about" element={<About />} />
              <Route path="/iletisim" element={<Iletisim />} />
            </Routes>
            <Footer />
          </div>
        </div>
      </div>

      <style>{`
        .sidebar-history-item:hover { background: rgba(0,0,0,0.04) !important; color: var(--text-main) !important; }
        .top-nav-link:hover { background: rgba(0,0,0,0.04) !important; color: var(--text-main) !important; }
        .admin-link:hover { background: rgba(0,0,0,0.04) !important; color: var(--text-main) !important; }
      `}</style>
    </Router>
  );
}

export default App;
