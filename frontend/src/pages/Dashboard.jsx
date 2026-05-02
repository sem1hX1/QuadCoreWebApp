import React, { useState } from 'react';
import { Search, TrendingUp, DollarSign, Clock, ShieldCheck, ArrowRight, ExternalLink, Cpu, BarChart3, PieChart as PieChartIcon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { searchComponents, analyzeComponent } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const Dashboard = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery) return;
    setLoading(true);
    try {
      const data = await searchComponents(searchQuery);
      setResults(data);
      setAnalysis(null);
    } catch (error) {
      console.error("Arama hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async (component) => {
    setAnalyzing(true);
    try {
      const data = await analyzeComponent(component);
      setAnalysis(data);
    } catch (error) {
      console.error("Analiz hatası:", error);
    } finally {
      setAnalyzing(false);
    }
  };

  const stats = [
    { label: 'Analiz Edilen Parça', value: '1.2k+', icon: <TrendingUp size={20} />, color: '#3b82f6' },
    { label: 'Ort. Tasarruf', value: '%24', icon: <DollarSign size={20} />, color: '#10b981' },
    { label: 'Tedarik Süresi', value: '3-5 Gün', icon: <Clock size={20} />, color: '#8b5cf6' },
    { label: 'Güvenilir Satıcı', value: '48+', icon: <ShieldCheck size={20} />, color: '#f59e0b' },
  ];

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <div style={{ textAlign: 'center', padding: '60px 0 40px 0' }}>
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 style={{ fontSize: '3.5rem', fontWeight: '800', marginBottom: '15px', background: 'linear-gradient(to right, #fff, var(--primary))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Geleceğin Tedarik Zinciri
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', maxWidth: '700px', margin: '0 auto 40px auto', lineHeight: '1.6' }}>
            Yapay zeka ile milyonlarca komponenti saniyeler içinde tarayın, en iyi fiyat ve lojistik rotasını anında bulun.
          </p>
        </motion.div>

        {/* Main Search Bar - Hero Style */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="glass-card" 
          style={{ maxWidth: '800px', margin: '0 auto', padding: '10px', display: 'flex', gap: '10px', boxShadow: '0 0 50px rgba(59, 130, 246, 0.2)' }}
        >
          <div style={{ flex: 1, position: 'relative' }}>
            <Search style={{ position: 'absolute', left: '20px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} size={24} />
            <input 
              type="text" 
              className="input-glass" 
              placeholder="Parça kodu veya teknik özellik girin (Örn: STM32, ESP32...)" 
              style={{ width: '100%', padding: '15px 15px 15px 60px', fontSize: '1.1rem', border: 'none' }}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <button 
            className="premium-button" 
            style={{ padding: '0 40px', fontSize: '1.1rem' }}
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? 'Analiz Ediliyor...' : 'Akıllı Tarama'}
          </button>
        </motion.div>
      </div>

      {/* Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '60px', marginTop: '20px' }}>
        {stats.map((stat, index) => (
          <motion.div 
            key={index}
            whileHover={{ y: -5 }}
            className="glass-card" 
            style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '10px' }}
          >
            <div style={{ color: stat.color }}>{stat.icon}</div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{stat.label}</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{stat.value}</div>
          </motion.div>
        ))}
      </div>

      {/* Results Section */}
      <div style={{ display: 'grid', gridTemplateColumns: analysis ? '1fr 1fr' : '1fr', gap: '30px' }}>
        {/* Component List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <AnimatePresence>
            {results.map((comp) => (
              <motion.div 
                layout
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                key={comp.id}
                className="glass-card"
                style={{ padding: '20px' }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '5px' }}>{comp.name}</h3>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{comp.category}</span>
                  </div>
                  <button 
                    className="premium-button" 
                    style={{ padding: '8px 16px', fontSize: '0.9rem' }}
                    onClick={() => handleAnalyze(comp)}
                  >
                    AI İncelemesi <ArrowRight size={16} />
                  </button>
                </div>
                
                <div style={{ marginTop: '15px', display: 'flex', gap: '20px' }}>
                  {comp.sources.map(source => (
                    <div key={source.site} style={{ fontSize: '0.85rem' }}>
                      <span style={{ fontWeight: 'bold' }}>{source.site}:</span> ${source.price}
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {results.length === 0 && !loading && (
            <div style={{ textAlign: 'center', padding: '60px', color: 'var(--text-muted)' }}>
              <p>Henüz bir sonuç yok. Başlamak için yukarıdaki kutuyu kullanın.</p>
            </div>
          )}
        </div>

        {/* AI Analysis View */}
        {analysis && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card"
            style={{ padding: '30px', border: '1px solid var(--primary)', position: 'sticky', top: '100px', height: 'fit-content' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary)' }}>
                <Cpu size={24} />
                <h3 style={{ fontSize: '1.5rem' }}>AI Kararı</h3>
              </div>
              <div style={{ fontSize: '0.8rem', padding: '4px 10px', background: 'rgba(59, 130, 246, 0.2)', borderRadius: '20px', color: 'var(--primary)' }}>
                Yüksek Güven
              </div>
            </div>
            
            <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '20px', borderRadius: '12px', marginBottom: '25px', borderLeft: '4px solid var(--primary)' }}>
              <p style={{ lineHeight: '1.6', fontSize: '0.95rem' }}>{analysis.summary}</p>
            </div>

            {/* Charts Section */}
            <div style={{ height: '200px', marginBottom: '30px' }}>
              <h4 style={{ fontSize: '0.9rem', marginBottom: '15px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <BarChart3 size={16} /> Fiyat Karşılaştırması ($)
              </h4>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={analysis.charts.priceData}>
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ background: '#1e293b', border: '1px solid var(--glass-border)', borderRadius: '8px' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Bar dataKey="fiyat" radius={[4, 4, 0, 0]}>
                    {analysis.charts.priceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === analysis.recommendation.site ? '#3b82f6' : 'rgba(255,255,255,0.2)'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid var(--glass-border)' }}>
                <span style={{ color: 'var(--text-muted)' }}>En İyi Tedarikçi</span>
                <span style={{ fontWeight: 'bold', color: 'var(--accent)' }}>{analysis.recommendation.site}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid var(--glass-border)' }}>
                <span style={{ color: 'var(--text-muted)' }}>Birim Fiyat</span>
                <span style={{ fontWeight: 'bold' }}>${analysis.recommendation.price}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid var(--glass-border)' }}>
                <span style={{ color: 'var(--text-muted)' }}>Stok Durumu</span>
                <span style={{ fontWeight: 'bold' }}>{analysis.recommendation.stock} Adet</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid var(--glass-border)' }}>
                <span style={{ color: 'var(--text-muted)' }}>Tahmini Teslim</span>
                <span style={{ fontWeight: 'bold' }}>{analysis.recommendation.shipping}</span>
              </div>
            </div>

            <button className="premium-button" style={{ width: '100%', marginTop: '30px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px', height: '50px' }}>
              Satın Alma Sayfasına Git <ExternalLink size={18} />
            </button>
          </motion.div>
        )}

        {analyzing && (
          <div className="glass-card" style={{ padding: '40px', textAlign: 'center' }}>
            <div className="loader" style={{ marginBottom: '20px' }}></div>
            <p>AI Verileri Analiz Ediyor...</p>
          </div>
        )}
      </div>
      
      <style dangerouslySetInnerHTML={{ __html: `
        .loader {
          border: 4px solid rgba(255, 255, 255, 0.1);
          border-left-color: var(--primary);
          border-radius: 50%;
          width: 40px;
          height: 40px;
          animation: spin 1s linear infinite;
          margin: 0 auto;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}} />

      {/* Why ComponentSource Section */}
      {!analysis && results.length === 0 && (
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          style={{ marginTop: '100px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px' }}
        >
          <div className="glass-card" style={{ padding: '30px' }}>
            <h4 style={{ fontSize: '1.2rem', marginBottom: '15px', color: 'var(--accent)' }}>Gerçek Zamanlı Analiz</h4>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>Dünyanın önde gelen 50'den fazla distribütörünü aynı anda tarar ve saniyeler içinde verileri önünüze serer.</p>
          </div>
          <div className="glass-card" style={{ padding: '30px' }}>
            <h4 style={{ fontSize: '1.2rem', marginBottom: '15px', color: 'var(--secondary)' }}>Yapay Zeka Karar Mekanizması</h4>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>Sadece en ucuzu değil; vergi, gümrük ve kargo süresini hesaplayarak en mantıklı satın alma rotasını önerir.</p>
          </div>
          <div className="glass-card" style={{ padding: '30px' }}>
            <h4 style={{ fontSize: '1.2rem', marginBottom: '15px', color: 'var(--primary)' }}>Tedarik Risk Analizi</h4>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>Satıcıların güvenilirlik puanlarını ve stok trendlerini analiz ederek sizi yarı yolda bırakmayacak kaynakları seçer.</p>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Dashboard;
