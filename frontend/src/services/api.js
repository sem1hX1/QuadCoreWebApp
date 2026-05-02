import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const SUPPLIER_COLORS = {
  DigiKey: '#e53935',
  Mouser: '#1e88e5',
  LCSC: '#2e7d32',
  AliExpress: '#ff6d00',
  Trendyol: '#f57c00',
  Hepsiburada: '#ff8f00',
  Amazon: '#ffa000',
};

function transformToCards(analysisResponse) {
  const { results, best_deal, suggested_price } = analysisResponse;
  const aiHint = `En iyi teklif: ${best_deal.source} ($${best_deal.price.toFixed(2)}), Önerilen: $${suggested_price.toFixed(2)}`;

  return results.map((item, index) => ({
    id: index + 1,
    name: item.title,
    supplier: item.source,
    supplierColor: SUPPLIER_COLORS[item.source] || '#607d8b',
    price: item.price,
    stock: item.region === 'TR' ? 'TR Pazar' : 'Global Stok',
    status: item.region === 'TR' ? 'TR' : 'Global',
    ai: aiHint,
    category: item.brand || 'Elektronik',
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
