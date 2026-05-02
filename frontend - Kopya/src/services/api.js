import axios from 'axios';

// Backend ekibinin sunucu adresi (burayı onlara göre güncelleyebilirsin)
const API_URL = 'http://localhost:5000/api';

// Frontend geliştirme sırasında backend hazır değilse mock verileri kullan
const USE_MOCK = true; 

const mockResults = [
  { id: 101, name: 'STM32F103C8T6', supplier: 'Mouser', supplierColor: '#1e88e5', price: 4.50, stock: '1.2K', status: 'Stok', ai: 'LCSC ($3.80, 7-12 Gün)', category: 'ARM MCU' },
  { id: 102, name: 'STM32F103RET6', supplier: 'Digi-Key', supplierColor: '#e53935', price: 6.20, stock: 450, status: 'Az Stok', ai: 'Mouser ($6.00, Stok Teslim)', category: 'ARM MCU' },
  { id: 103, name: 'ESP32-WROOM-32D', supplier: 'LCSC', supplierColor: '#ff6d00', price: 3.20, stock: '5K+', status: 'Stok', ai: 'LCSC ($3.20, En Uygun)', category: 'WiFi+BT MCU' },
  { id: 104, name: 'LM317T', supplier: 'Mouser', supplierColor: '#1e88e5', price: 0.45, stock: '10K+', status: 'Stok', ai: 'AliExpress ($0.15, Yavaş Teslimat)', category: 'Regülatör' },
  { id: 105, name: 'ATMEGA328P-PU', supplier: 'Digi-Key', supplierColor: '#e53935', price: 2.10, stock: 800, status: 'Stok', ai: 'Mouser ($2.00, Hızlı Teslimat)', category: '8-bit MCU' }
];

export const searchComponents = async (query) => {
  if (USE_MOCK) {
    await new Promise(r => setTimeout(r, 800));
    return mockResults.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));
  }
  const response = await axios.get(`${API_URL}/search?q=${query}`);
  return response.data;
};

export const analyzeComponent = async (componentData) => {
  if (USE_MOCK) {
    await new Promise(r => setTimeout(r, 1500));
    return {
      recommendation: componentData.sources[0],
      summary: "AI Analizi: Stok ve fiyat dengesi açısından en uygun seçenek Mouser.",
      charts: {
        priceData: componentData.sources.map(s => ({ name: s.site, fiyat: s.price }))
      }
    };
  }
  const response = await axios.post(`${API_URL}/analyze`, { componentData });
  return response.data;
};

// Admin panelini yapacak arkadaş için ayarlar servisleri
export const getSettings = async () => {
  const response = await axios.get(`${API_URL}/settings`);
  return response.data;
};
