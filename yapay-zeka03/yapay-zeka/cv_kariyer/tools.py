import fitz  # pymupdf
from docx import Document
import os

def cv_oku(dosya_yolu: str) -> str:
    """PDF veya DOCX formatındaki CV'yi okur ve metin olarak döndürür."""
    
    if not os.path.exists(dosya_yolu):
        return f"Hata: Dosya bulunamadı → {dosya_yolu}"
    
    uzanti = os.path.splitext(dosya_yolu)[1].lower()
    
    if uzanti == ".pdf":
        return _pdf_oku(dosya_yolu)
    elif uzanti in [".docx", ".doc"]:
        return _docx_oku(dosya_yolu)
    else:
        return f"Hata: Desteklenmeyen dosya formatı → {uzanti}"


def _pdf_oku(dosya_yolu: str) -> str:
    """PDF dosyasını okur."""
    try:
        metin = ""
        doc = fitz.open(dosya_yolu)
        for sayfa in doc:
            metin += sayfa.get_text()
        doc.close()
        
        if not metin.strip():
            return "Hata: PDF'den metin çıkarılamadı (taranmış görsel olabilir)"
        
        return metin.strip()
    except Exception as e:
        return f"PDF okuma hatası: {str(e)}"


def _docx_oku(dosya_yolu: str) -> str:
    """DOCX dosyasını okur."""
    try:
        doc = Document(dosya_yolu)
        metin = "\n".join([paragraf.text for paragraf in doc.paragraphs])
        
        if not metin.strip():
            return "Hata: DOCX'ten metin çıkarılamadı"
        
        return metin.strip()
    except Exception as e:
        return f"DOCX okuma hatası: {str(e)}"


def cv_analiz_hazirla(cv_metni: str, ilan_metni: str = "") -> str:
    from datetime import datetime
    bugun = datetime.now().strftime("%d %B %Y")
    
    prompt = f"""Bugünün tarihi: {bugun}. Tüm tarih yorumlarını buna göre yap.
CV'deki tarihleri değerlendirirken bu tarihi referans al — hangi deneyimler devam ediyor, hangisi geçmişte kaldı buna göre belirt.

Aşağıdaki CV'yi analiz et ve şunları belirt:

1. **Kişisel Bilgiler**: İsim, iletişim bilgileri
2. **Deneyim**: İş geçmişi ve süreler
3. **Eğitim**: Okul ve bölüm bilgileri  
4. **Beceriler**: Teknik ve soft skills
5. **Güçlü Yönler**: CV'nin öne çıkan artıları
6. **Geliştirilecek Alanlar**: Eksik veya zayıf noktalar

CV METNİ:
{cv_metni}
"""
    
    if ilan_metni:
        prompt += f"""
7. **İş İlanı Uyumu**: Aşağıdaki iş ilanıyla ne kadar örtüşüyor?

İŞ İLANI:
{ilan_metni}
"""
    return prompt