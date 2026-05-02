from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="QuadCore API", version="1.0.0")

# CORS ayarları (Frontend ile konuşabilmek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "QuadCore Backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
