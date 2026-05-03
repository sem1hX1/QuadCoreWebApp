from backend.app.db.session import engine
from backend.app.db.models import Base
from sqlalchemy import text

def clear_db():
    print("Veritabanı temizleniyor...")
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            # Tabloları sil ve yeniden oluştur (en temizi)
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            transaction.commit()
            print("Tüm veriler başarıyla silindi ve tablolar sıfırlandı.")
        except Exception as e:
            transaction.rollback()
            print(f"Hata: {e}")

if __name__ == "__main__":
    clear_db()
