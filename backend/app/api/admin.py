from fastapi import APIRouter, HTTPException
from typing import List, Dict
import os
import re

router = APIRouter(prefix="/admin", tags=["Admin & Logs"])

LOG_FILE = "app.log"

@router.get("/logs", response_model=List[Dict])
async def get_logs():
    """app.log dosyasındaki gerçek sistem loglarını okur ve JSON olarak döner."""
    if not os.path.exists(LOG_FILE):
        return []

    logs = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
            # Son 200 logu al
            for i, line in enumerate(lines[-200:]):
                # Format: 2026-05-02 21:05:44,123 [INFO] app.main: Mesaj
                match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?\[(INFO|WARNING|ERROR|DEBUG)\] (.*?): (.*)", line)
                if match:
                    logs.append({
                        "id": i,
                        "timestamp": match.group(1),
                        "level": match.group(2),
                        "source": match.group(3),
                        "message": match.group(4).strip()
                    })
                else:
                    # Format uymuyorsa düz metin olarak ekle
                    logs.append({
                        "id": i,
                        "timestamp": "N/A",
                        "level": "INFO",
                        "source": "System",
                        "message": line.strip()
                    })
        
        return logs[::-1] # En yeni en üstte
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Log dosyası okunurken hata: {str(e)}")
