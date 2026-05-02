import React from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="animate-fade-in" 
      style={{ padding: '40px 20px', maxWidth: '1000px', margin: '0 auto' }}
    >
      <h1 style={{ fontSize: '3rem', marginBottom: '40px', color: 'var(--text-main)', textAlign: 'center' }}>Hakkımızda</h1>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '80px' }}>
        <section className="glass-card" style={{ padding: '60px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '2rem', marginBottom: '20px' }}>Biz Kimiz?</h2>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.8', fontSize: '1.1rem' }}>
              ComponentSource, elektronik donanım geliştiricileri ve satın alma departmanları için geliştirilmiş, 
              dünya çapındaki tüm büyük komponent distribütörlerini tek bir ekranda toplayan profesyonel bir analiz aracıdır.
              Elektronik üretim süreçlerindeki tedarik zinciri darboğazlarını bizzat yaşamış, yazılım ve donanım mühendislerinden oluşan tutkulu bir ekibiz.
            </p>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', height: '250px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--glass-border)' }}>
            <Search size={64} color="var(--text-muted)" opacity={0.3} />
          </div>
        </section>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
          <section className="glass-card" style={{ padding: '40px' }}>
            <h3 style={{ fontSize: '1.8rem', marginBottom: '15px', color: 'var(--primary)' }}>Misyonumuz</h3>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>
              Donanım geliştiricilerinin en iyi parçaları, en doğru fiyata ve en hızlı şekilde bulmasını sağlayarak, 
              küresel çapta inovasyonun önündeki lojistik engelleri kaldırmak.
            </p>
          </section>

          <section className="glass-card" style={{ padding: '40px' }}>
            <h3 style={{ fontSize: '1.8rem', marginBottom: '15px', color: 'var(--primary)' }}>Vizyonumuz</h3>
            <p style={{ color: 'var(--text-muted)', lineHeight: '1.6' }}>
              Dünyadaki tüm elektronik bileşen tedarik zincirini tek bir otonom platformda birleştirerek, 
              geleceğin fabrikaları ve Ar-Ge merkezleri için endüstri standardı olmak.
            </p>
          </section>
        </div>
      </div>
      
      {/* Footer */}
      <footer style={{ marginTop: '100px', paddingTop: '40px', borderTop: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        <div>
          &copy; 2026 ComponentSource. Tüm Hakları Saklıdır.
        </div>
        <div style={{ display: 'flex', gap: '20px' }}>
          <span style={{ cursor: 'pointer' }}>Gizlilik Politikası</span>
          <span style={{ cursor: 'pointer' }}>Kullanım Şartları</span>
          <span style={{ cursor: 'pointer' }}>İletişim</span>
        </div>
      </footer>
    </motion.div>
  );
};

export default About;
