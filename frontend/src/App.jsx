import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { LayoutDashboard, Cpu } from 'lucide-react';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="bg-gradient"></div>
      <div className="app-container">
        <nav className="glass-card" style={{ 
          margin: '20px', 
          padding: '15px 30px', 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          position: 'sticky',
          top: '20px',
          zIndex: 100
        }}>
          <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none', color: 'inherit' }}>
            <Cpu size={32} color="var(--primary)" />
            <span className="brand" style={{ fontSize: '1.5rem', fontWeight: 'bold', letterSpacing: '1px' }}>
              COMPONENT<span style={{ color: 'var(--primary)' }}>SOURCE</span> AI
            </span>
          </Link>
          
          <div style={{ display: 'flex', gap: '30px' }}>
            <Link to="/" className="nav-link">
              <LayoutDashboard size={20} />
              <span>Dashboard</span>
            </Link>
          </div>
        </nav>

        <main style={{ padding: '0 20px 40px 20px', maxWidth: '1400px', margin: '0 auto' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </main>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        .nav-link {
          display: flex;
          align-items: center;
          gap: 8px;
          text-decoration: none;
          color: var(--text-muted);
          font-weight: 500;
          transition: all 0.3s ease;
        }
        .nav-link:hover {
          color: var(--primary);
        }
        .nav-link svg {
          transition: transform 0.3s ease;
        }
        .nav-link:hover svg {
          transform: translateY(-2px);
        }
      `}} />
    </Router>
  );
}

export default App;
