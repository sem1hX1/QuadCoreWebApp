// Para birimi state'i — global, localStorage'a persist, custom event ile sync
import { useEffect, useState } from 'react';
import apiClient from './api';

const STORAGE_KEY = 'qc_currency';
const RATES_STORAGE_KEY = 'qc_currency_rates';

// Varsayılan kurlar — backend ulaşılamazsa fallback
const DEFAULT_RATES = {
  TRY: 1,
  EUR: 0.0189, // 1 TRY ≈ 0.0189 EUR (yaklaşık)
  USD: 0.0221, // 1 TRY ≈ 0.0221 USD
};

const SYMBOLS = { TRY: '₺', EUR: '€', USD: '$' };

let _currency = (typeof window !== 'undefined' && localStorage.getItem(STORAGE_KEY)) || 'TRY';
let _rates = (() => {
  try {
    const cached = localStorage.getItem(RATES_STORAGE_KEY);
    if (cached) return { ...DEFAULT_RATES, ...JSON.parse(cached) };
  } catch {}
  return { ...DEFAULT_RATES };
})();

const EVT = 'qcCurrencyUpdated';

export function getCurrency() {
  return _currency;
}

export function getRates() {
  return _rates;
}

export function setCurrency(c) {
  if (!['TRY', 'EUR', 'USD'].includes(c)) return;
  _currency = c;
  try { localStorage.setItem(STORAGE_KEY, c); } catch {}
  window.dispatchEvent(new CustomEvent(EVT));
}

export async function fetchRates() {
  try {
    const r = await apiClient.get('/products/currency-rates', { timeout: 8000 });
    const data = r.data || {};
    if (data.EUR && data.USD) {
      _rates = { TRY: 1, EUR: Number(data.EUR), USD: Number(data.USD) };
      try { localStorage.setItem(RATES_STORAGE_KEY, JSON.stringify(_rates)); } catch {}
      window.dispatchEvent(new CustomEvent(EVT));
    }
  } catch (e) {
    // Sessizce default'larla devam
  }
}

// React hook — tüm bileşenler currency değişimine reaktif
export function useCurrency() {
  const [currency, setCurrencyState] = useState(_currency);
  const [rates, setRatesState] = useState(_rates);

  useEffect(() => {
    const handler = () => {
      setCurrencyState(_currency);
      setRatesState({ ..._rates });
    };
    window.addEventListener(EVT, handler);
    return () => window.removeEventListener(EVT, handler);
  }, []);

  return { currency, rates, setCurrency, symbol: SYMBOLS[currency] || '₺' };
}

// TRY tutarını verilen hedef para birimine çevirir
export function convertFromTRY(tryAmount, target = _currency, ratesOverride = _rates) {
  if (typeof tryAmount !== 'number' || isNaN(tryAmount)) return 0;
  const r = ratesOverride[target];
  if (!r) return tryAmount; // bilinmeyen → TRY göster
  return tryAmount * r;
}

// Bir ürün nesnesinin TRY karşılığını al — tutarlılık için tek yerden okunur
export function priceTRY(item) {
  if (!item) return 0;
  return Number(item.price_try ?? item.price ?? 0) || 0;
}

// Currency-aware fiyat formatı
// Örn: TRY → "₺125.40", EUR → "€2.36", USD → "$2.78"
export function formatInCurrency(tryAmount, target = _currency, ratesOverride = _rates) {
  const value = convertFromTRY(tryAmount, target, ratesOverride);
  const symbol = SYMBOLS[target] || '₺';
  return `${symbol}${value.toFixed(2)}`;
}

// Bir ürünü direkt formatla (TR ve Global aynı şekilde, sadece seçili currency'de)
export function formatProductPrice(item, target = _currency, ratesOverride = _rates) {
  return formatInCurrency(priceTRY(item), target, ratesOverride);
}

export const SUPPORTED_CURRENCIES = ['TRY', 'EUR', 'USD'];
export { SYMBOLS };
