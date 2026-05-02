import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const SUPPLIER_COLORS = {
  DigiKey: '#e53935',
  Mouser: '#1e88e5',
  LCSC: '#2e7d32',
  Farnell: '#ff6600',
  Arrow: '#007bc4',
};

function transformToCards(aiAnalysisList) {
  if (!aiAnalysisList || aiAnalysisList.length === 0) return [];
  
  // İlk analiz sonucunu baz alıyoruz (veya hepsini birleştirebiliriz)
  const analysis = aiAnalysisList[0];
  const { top3, market_refs, pricing, ref_suggestion } = analysis;
  
  // Tüm ürünleri (top3 + market_refs) tek bir listede birleştiriyoruz
  const allResults = [...top3, ...market_refs];
  
  const aiHint = `AI Önerisi: $${pricing.price} (Kar Marjı: %${(pricing.margin * 100).toFixed(1)})`;

  return allResults.map((item, index) => ({
    id: index + 1,
    name: item.title,
    supplier: item.source,
    supplierColor: SUPPLIER_COLORS[item.source] || '#607d8b',
    price: item.price,
    stock: item.region === 'TR' ? 'TR Pazar' : 'Global Stok',
    status: item.region === 'TR' ? 'TR' : 'Global',
    ai: aiHint,
    category: 'Elektronik',
    url: item.url,
    // Ek veriler (detay paneli için)
    description: analysis.description,
    ref_suggestion: analysis.ref_suggestion
  }));
}

export const searchComponents = async (query) => {
  const { data } = await axios.get(`${BASE_URL}/products/search`, {
    params: { q: query },
  });
  return transformToCards(data);
};

export const analyzeComponent = async (productId) => {
  const { data } = await axios.post(`${BASE_URL}/products/${productId}/analyze`);
  return data;
};
