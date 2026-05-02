import axios from 'axios';

// FastAPI Backend adresi
const API_URL = 'http://localhost:8000';
// Mock/Ayarlar Servisi (Express) adresi
const SETTINGS_URL = 'http://localhost:5000/api';

// Gerçek backend bağlantısı için false yapıldı
const USE_MOCK = false; 

/**
 * Ürün arama fonksiyonu.
 * FastAPI tarafında /products endpoint'ini kullanarak veritabanındaki ürünleri listeler.
 * Eğer ürün yoksa yeni bir ürün oluşturulup arama yapılabilir.
 */
export const searchComponents = async (query) => {
  if (USE_MOCK) {
    await new Promise(r => setTimeout(r, 800));
    return [];
  }
  
  try {
    // Önce mevcut ürünleri getir
    const response = await axios.get(`${API_URL}/products/`);
    const results = response.data;
    
    // Query'e göre filtrele
    const filtered = results.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));
    
    // Eğer veritabanında bu isimde bir ürün yoksa ve kullanıcı bir şey arıyorsa, 
    // otomatik olarak yeni bir ürün kaydı oluşturup onu döndürebiliriz (veya boş döneriz)
    if (filtered.length === 0 && query.length > 2) {
      const createRes = await axios.post(`${API_URL}/products/`, { name: query });
      return [createRes.data];
    }
    
    return filtered;
  } catch (error) {
    console.error("Search error:", error);
    return [];
  }
};

/**
 * Ürün analizi fonksiyonu.
 * FastAPI /products/{id}/analyze endpoint'ini kullanır.
 */
export const analyzeComponent = async (componentData) => {
  if (USE_MOCK) {
    await new Promise(r => setTimeout(r, 1500));
    return {};
  }

  try {
    const response = await axios.post(`${API_URL}/products/${componentData.id}/analyze`);
    const data = response.data;

    // Frontend'in beklediği formata dönüştür
    return {
      recommendation: data.best_deal,
      summary: `AI Analizi: ${componentData.name} için önerilen satış fiyatı ${data.suggested_price} ${data.best_deal.currency}.`,
      charts: {
        priceData: data.results.map(r => ({ name: r.source, fiyat: r.price }))
      }
    };
  } catch (error) {
    console.error("Analysis error:", error);
    throw error;
  }
};

// Ayarlar servisi Express mock sunucusundan devam ediyor
export const getSettings = async () => {
  const response = await axios.get(`${SETTINGS_URL}/settings`);
  return response.data;
};

