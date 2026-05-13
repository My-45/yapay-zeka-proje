import json
import os
from datetime import datetime

HAFIZA_DOSYASI = "data/hafiza.json"


def hafizayi_yukle() -> dict:
    """Kaydedilmiş hafızayı yükler."""
    if os.path.exists(HAFIZA_DOSYASI):
        with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"analizler": [], "sohbet_gecmisi": []}


def hafizayi_kaydet(hafiza: dict):
    """Hafızayı dosyaya kaydeder."""
    os.makedirs("data", exist_ok=True)
    with open(HAFIZA_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(hafiza, f, ensure_ascii=False, indent=2)


def analiz_kaydet(cv_dosyasi: str, analiz_sonucu: str):
    """Yeni bir CV analizini hafızaya kaydeder."""
    hafiza = hafizayi_yukle()
    
    yeni_analiz = {
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "cv_dosyasi": cv_dosyasi,
        "sonuc": analiz_sonucu
    }
    
    hafiza["analizler"].append(yeni_analiz)
    hafizayi_kaydet(hafiza)
    print(f"Analiz kaydedildi: {cv_dosyasi}")


def sohbet_ekle(rol: str, mesaj: str):
    """Sohbet geçmişine mesaj ekler."""
    hafiza = hafizayi_yukle()
    
    hafiza["sohbet_gecmisi"].append({
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "rol": rol,
        "mesaj": mesaj
    })
    
    hafizayi_kaydet(hafiza)


def gecmis_analizleri_getir() -> list:
    """Geçmiş analizleri döndürür."""
    hafiza = hafizayi_yukle()
    return hafiza.get("analizler", [])


def sohbet_gecmisini_getir() -> list:
    """Sohbet geçmişini döndürür."""
    hafiza = hafizayi_yukle()
    return hafiza.get("sohbet_gecmisi", [])


def hafizayi_temizle():
    """Tüm hafızayı siler."""
    hafizayi_kaydet({"analizler": [], "sohbet_gecmisi": []})
    print("Hafıza temizlendi.")


# Test için
if __name__ == "__main__":
    print("memory.py başarıyla yüklendi!")
    
    # Test
    sohbet_ekle("kullanici", "Merhaba!")
    sohbet_ekle("asistan", "Merhaba! CV analizi için hazırım.")
    
    gecmis = sohbet_gecmisini_getir()
    print(f"Sohbet geçmişi: {len(gecmis)} mesaj var")
    print("Hafıza testi başarılı! ✓")