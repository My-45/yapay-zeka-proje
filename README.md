# 📄 CV Kariyer Asistanı

Yapay zeka destekli CV analiz ve kariyer danışmanlığı uygulaması.
Python ve Streamlit kullanılarak geliştirilmiştir.

---

## 🚀 Özellikler

- **CV Analizi** : Güçlü yönler ve eksikleri tespit eder
- **ATS Uyum Analizi** : CV ile iş ilanı uyumunu ölçer  
- **Kariyer Yolu** : Kısa, orta ve uzun vadeli kariyer önerileri sunar
- **Kurs Önerileri** :Kullanıcıya uygun kurs önerileri verir. (Coursera, Udemy, Btk Akademi)
- **Sohbet** : CV hakkında serbest soru sorulmasına olanak tanır
-**Geçmiş** : Geçmişte yapılan analizleri listeler.
---

## 🛠️ Kullanılan Teknolojiler

| Kütüphane | Amaç |
|-----------|------|
| Streamlit | Web arayüzü |
| Google Gemini 2.5 Flash | Yapay zeka modeli |
| PyMuPDF | PDF okuma |
| python-docx | DOCX okuma |
| python-dotenv | API anahtarı yönetimi |

---

## ⚙️ Kurulum

**1. Repoyu klonlayın**

```bash
git clone https://github.com/My-45/yapay-zeka-proje.git
cd yapay-zeka-proje/yapay-zeka03/yapay-zeka/cv_kariyer
```

**2. Kütüphaneleri yükleyin**

```bash
pip install -r requirements.txt
```

**3. API anahtarını ekleyin**

`.env` adında bir dosya oluşturun ve şunu yazın:
> API anahtarı almak için → [aistudio.google.com](https://aistudio.google.com)

**4. Uygulamayı başlatın**

```bash
streamlit run app.py
```
---
Tarayıcıda otomatik açılacaktır. 
## 📁 Proje Yapısı

cv_kariyer/
├── agent.py           ← Yapay zeka fonksiyonları
├── tools.py           ← CV okuma araçları
├── memory.py          ← Bellek yönetimi
├── app.py             ← Streamlit arayüzü
├── web_course_tool.py ← Web arama aracı
├── requirements.txt   ← Kütüphane listesi
└── .env               ← API anahtarı 

---

## 🖥️ Kullanım

1. Uygulamayı başlatın
2. **CV Analizi** sekmesinden CV dosyanızı yükleyin
3. İsterseniz iş ilanı metnini yapıştırın
4. **Analiz Başlat** butonuna tıklayın
5. Diğer sekmeleri kullanarak kariyer yolu , ATS analizi , kurs önerileri , sohbet ve geçmiş özelliklerinden yararlanabilirsiniz

---



## 👥 Geliştirici Ekip

Merve YILMAZ
RANİA KAZZIHA
ZEYNEP BAYRAKTAR
---

## ⚠️ Notlar

- Ücretsiz Gemini API katmanında günlük istek limiti bulunmaktadır
- Python 3.9 veya üzeri gereklidir
