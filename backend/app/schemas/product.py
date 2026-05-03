from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MarketProduct(BaseModel):
    """Görseldeki veri modeline tam uyumlu ürün yapısı."""
    title: str = Field(..., description="Ürün başlığı")
    brand: str = Field(..., description="Marka")
    price: float = Field(..., description="Fiyat")
    currency: str = Field(..., description="Para birimi (USD, TRY vb.)")
    region: str = Field(..., description="Bölge (global, TR vb.)")
    source: str = Field(..., description="Veri kaynağı (Mouser, DigiKey vb.)")
    url: Optional[str] = Field(None, description="Ürün kaynak adresi")

class ProductBase(BaseModel):
    name: str = Field(..., description="Ürünün aranan adı veya parça numarası")
    sku: Optional[str] = Field(None, description="Stok Kodu")

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PricingInfo(BaseModel):
    status: str
    price: Optional[float] = None
    margin: Optional[float] = None

class AIProductInfo(BaseModel):
    title: str
    source: str
    region: str
    price: float
    price_try: float
    url: Optional[str] = None

class AIAnalysisResult(BaseModel):
    product: str
    cost: float
    pricing: PricingInfo
    ref_suggestion: str
    top3: List[AIProductInfo]
    market_refs: List[AIProductInfo]
    description: str

class AnalysisResponse(BaseModel):
    # Bu şema artık bir liste içerebilir veya direkt liste dönebiliriz
    # FastAPI'de List[AIAnalysisResult] kullanacağız
    pass
