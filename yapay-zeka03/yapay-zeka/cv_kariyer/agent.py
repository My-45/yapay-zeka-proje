from google import genai
from dotenv import load_dotenv
import os
from tools import cv_oku, cv_analiz_hazirla
from web_course_tool import kurslari_webde_ara

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def cv_analiz_et(dosya_yolu: str, ilan_metni: str = "") -> str:
    """CV dosyasını okur ve Gemini ile analiz eder."""
    print(f"CV okunuyor: {dosya_yolu}")
    cv_metni = cv_oku(dosya_yolu)
    if cv_metni.startswith("Hata:"):
        return cv_metni
    print("Gemini ile analiz yapılıyor...")
    prompt = cv_analiz_hazirla(cv_metni, ilan_metni)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text


def soru_sor(cv_metni: str, soru: str) -> str:
    """CV hakkında özel bir soru sorar."""
    from datetime import datetime
    bugun = datetime.now().strftime("%d %B %Y")
    prompt = f"""Bugünün tarihi: {bugun}. Tüm tarih yorumlarını buna göre yap.

Aşağıdaki CV'yi inceleyerek soruyu yanıtla.

CV:
{cv_metni}

SORU: {soru}
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text


def ats_analiz_et(cv_metni: str, ilan_metni: str) -> dict:
    """CV'yi iş ilanıyla ATS uyumu açısından analiz eder. JSON döner."""
    from datetime import datetime
    bugun = datetime.now().strftime("%d %B %Y")

    prompt = f"""Bugünün tarihi: {bugun}.

Aşağıdaki CV ile iş ilanını ATS (Applicant Tracking System) uyumu açısından analiz et.

Yalnızca şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "ats_skoru": <0-100 arası sayı>,
  "eslesen_keywords": ["keyword1", "keyword2", ...],
  "eksik_keywords": ["keyword1", "keyword2", ...],
  "ozet": "2-3 cümlelik genel değerlendirme",
  "oneriler": ["öneri1", "öneri2", "öneri3"]
}}

CV:
{cv_metni}

İŞ İLANI:
{ilan_metni}
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    import json
    import re
    metin = response.text.strip()
    metin = re.sub(r"```json|```", "", metin).strip()
    
    try:
        return json.loads(metin)
    except:
        return {
            "ats_skoru": 0,
            "eslesen_keywords": [],
            "eksik_keywords": [],
            "ozet": metin,
            "oneriler": []
        }


def kariyer_yolu_analiz_et(cv_metni: str) -> dict:
    """CV'ye göre kariyer yolu önerileri oluşturur. JSON döner."""
    from datetime import datetime
    bugun = datetime.now().strftime("%d %B %Y")

    prompt = f"""Bugünün tarihi: {bugun}.

Aşağıdaki CV'yi analiz ederek kariyer yolu önerileri sun.

Yalnızca şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "mevcut_seviye": "Junior / Mid-level / Senior / Lead gibi",
  "mevcut_alan": "Kişinin çalıştığı alan",
  "kisa_vade": {{
    "sure": "0-1 yıl",
    "pozisyonlar": ["pozisyon1", "pozisyon2"],
    "gelismesi_gerekenler": ["beceri1", "beceri2"]
  }},
  "orta_vade": {{
    "sure": "1-3 yıl",
    "pozisyonlar": ["pozisyon1", "pozisyon2"],
    "gelismesi_gerekenler": ["beceri1", "beceri2"]
  }},
  "uzun_vade": {{
    "sure": "3-5 yıl",
    "pozisyonlar": ["pozisyon1", "pozisyon2"],
    "gelismesi_gerekenler": ["beceri1", "beceri2"]
  }},
  "guclu_yonler": ["güçlü yön 1", "güçlü yön 2", "güçlü yön 3"],
  "tavsiye": "Kişiye özel 2-3 cümlelik kariyer tavsiyesi"
}}

CV:
{cv_metni}
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

    import json
    import re
    metin = response.text.strip()
    metin = re.sub(r"```json|```", "", metin).strip()

    try:
        return json.loads(metin)
    except:
        return {
            "mevcut_seviye": "Belirlenemedi",
            "mevcut_alan": "Belirlenemedi",
            "kisa_vade": {"sure": "0-1 yıl", "pozisyonlar": [], "gelismesi_gerekenler": []},
            "orta_vade": {"sure": "1-3 yıl", "pozisyonlar": [], "gelismesi_gerekenler": []},
            "uzun_vade": {"sure": "3-5 yıl", "pozisyonlar": [], "gelismesi_gerekenler": []},
            "guclu_yonler": [],
            "tavsiye": metin
        }

def sertifika_kurs_oner(cv_metni: str) -> dict:
    """CV'yi analiz eder, web'den sertifikalı kurs/eğitim arar ve Gemini ile filtreleyip açıklar."""
    from datetime import datetime
    import json
    import re

    bugun = datetime.now().strftime("%d %B %Y")

    # 1) Önce CV'den kariyer yönü ve eksik becerileri çıkarıyoruz.
    kariyer_json = kariyer_yolu_analiz_et(cv_metni)

    # 2) Çıkan becerilere göre web araması yapıyoruz.
    web_sonuclari = kurslari_webde_ara(kariyer_json)

    if not web_sonuclari:
        return {
            "durum": "api_yok_veya_sonuc_yok",
            "mesaj": "Web araması yapılamadı. .env dosyasına TAVILY_API_KEY eklenmemiş olabilir veya arama sonucu dönmemiş olabilir.",
            "kariyer_analizi": kariyer_json,
            "oneriler": []
        }

    # 3) Bulunan linkleri Gemini'ye verip CV'ye en uygun olanları seçtiriyoruz.
    prompt = f"""Bugünün tarihi: {bugun}.

Aşağıdaki CV ve kariyer analizi için web'de bulunan kurs/eğitim sonuçlarını değerlendir.
Amaç: Kişinin kariyerinde ilerlemesine ve CV'sini güçlendirmesine en çok katkı sağlayacak sertifikalı kursları seçmek.

Yalnızca şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{
  "genel_degerlendirme": "Kişinin kariyeri için 2-3 cümlelik eğitim tavsiyesi",
  "oneriler": [
    {{
      "kurs_adi": "Kurs/eğitim adı",
      "platform": "Platform adı veya site adı",
      "link": "URL",
      "hedef_beceri": "Bu kurs hangi eksiği kapatıyor?",
      "neden_onerildi": "CV'ye göre neden mantıklı?",
      "cvye_katkisi": "CV'de nasıl güzel durur?",
      "uygunluk": "Başlangıç / Orta / İleri"
    }}
  ]
}}

Kurallar:
- En fazla 6 öneri seç.
- Linki olmayan sonucu kullanma.
- CV ile ilgisiz kursları ele.
- Sertifika/credential ihtimali yüksek olan platformları öne çıkar.
- Abartılı garanti verme; 'iş buldurur' gibi kesin ifadeler kullanma.

CV:
{cv_metni}

Kariyer analizi JSON:
{json.dumps(kariyer_json, ensure_ascii=False, indent=2)}

Web arama sonuçları:
{json.dumps(web_sonuclari, ensure_ascii=False, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    metin = response.text.strip()
    metin = re.sub(r"```json|```", "", metin).strip()

    try:
        sonuc = json.loads(metin)
    except Exception:
        sonuc = {
            "genel_degerlendirme": metin,
            "oneriler": []
        }

    sonuc["kariyer_analizi"] = kariyer_json
    sonuc["ham_web_sonuclari"] = web_sonuclari

    return sonuc


if __name__ == "__main__":
    print("agent.py başarıyla yüklendi!")
    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents="Merhaba, çalışıyor musun? Kısaca yanıtla.")
        print("Gemini API bağlantısı: ✓ Başarılı")
        print(f"Yanıt: {response.text}")
    except Exception as e:
        print(f"Gemini API hatası: {e}")