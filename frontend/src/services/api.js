import axios from 'axios';

// Backend ekibinin sunucu adresi (burayı onlara göre güncelleyebilirsin)
const API_URL = 'http://localhost:5000/api';

// Frontend geliştirme sırasında backend hazır değilse mock verileri kullan
const USE_MOCK = true; 

const mockResults = [
  {
    "id": "stm32f103",
    "name": "STM32F103C8T6",
    "category": "Microcontrollers",
    "sources": [
      { "site": "Mouser", "price": 4.50, "currency": "USD", "stock": 1200, "shipping": "2-3 Gün", "trustScore": 98 },
      { "site": "DigiKey", "price": 4.75, "currency": "USD", "stock": 800, "shipping": "2-4 Gün", "trustScore": 99 },
      { "site": "LCSC", "price": 3.80, "currency": "USD", "stock": 5000, "shipping": "7-12 Gün", "trustScore": 92 }
    ]
  }
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
