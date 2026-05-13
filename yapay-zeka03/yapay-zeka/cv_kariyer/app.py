import streamlit as st
import os
import tempfile
from datetime import datetime
from agent import cv_analiz_et, soru_sor, sertifika_kurs_oner ,kariyer_yolu_analiz_et, ats_analiz_et
from memory import analiz_kaydet, gecmis_analizleri_getir, sohbet_ekle, hafizayi_temizle
from tools import cv_oku

st.set_page_config(
    page_title="CV Asistan",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

bugun = datetime.now().strftime("%d %B %Y")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #dbb8ff 0%, #b3d4ff 30%, #ffb8d9 60%, #b3f0d4 100%);
    background-attachment: fixed;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(96,165,250,0.5) 0%, transparent 70%);
    top: -100px; left: -100px;
    border-radius: 50%;
    animation: float1 8s ease-in-out infinite;
    z-index: 0; pointer-events: none;
}
.stApp::after {
    content: '';
    position: fixed;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(96,165,250,0.3) 0%, transparent 70%);
    bottom: -80px; right: -80px;
    border-radius: 50%;
    animation: float2 10s ease-in-out infinite;
    z-index: 0; pointer-events: none;
}
@keyframes float1 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(60px, 40px) scale(1.1); }
}
@keyframes float2 {
    0%,100% { transform: translate(0,0) scale(1); }
    50% { transform: translate(-40px, -60px) scale(1.15); }
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.25) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.4) !important;
}
[data-testid="stSidebar"] * { color: #4a3f6b !important; }

.glass-card {
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 24px;
    padding: 32px 36px;
    box-shadow: 0 8px 32px rgba(120,80,200,0.1), inset 0 1px 0 rgba(255,255,255,0.8);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 20px;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(120,80,200,0.18), inset 0 1px 0 rgba(255,255,255,0.8);
}

.hero {
    background: rgba(255,255,255,0.3);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.65);
    border-radius: 28px;
    padding: 48px 52px;
    margin-bottom: 28px;
    box-shadow: 0 8px 40px rgba(120,80,200,0.12), inset 0 1px 0 rgba(255,255,255,0.9);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: 'CV';
    position: absolute;
    right: 40px; top: 20px;
    font-family: 'Playfair Display', serif;
    font-size: 7rem;
    font-weight: 800;
    opacity: 0.04;
    color: #7c3aed;
    line-height: 1;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 50%, #0891b2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin: 0 0 10px 0;
}
.hero-sub {
    color: #6b7280;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}
.hero-date {
    display: inline-block;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 30px;
    padding: 6px 18px;
    font-size: 0.8rem;
    color: #7c3aed;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}

.stat-row { display: flex; gap: 16px; margin-bottom: 24px; }
.stat-glass {
    flex: 1;
    background: rgba(255,255,255,0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 20px;
    padding: 22px 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(120,80,200,0.08);
    transition: transform 0.25s ease;
}
.stat-glass:hover { transform: translateY(-3px); }
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-lbl {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-top: 4px;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.35) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 16px !important;
    padding: 6px !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
    padding: 10px 26px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.85) !important;
    color: #7c3aed !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 12px rgba(124,58,237,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.35) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.5) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.4) !important;
    border: 2px dashed rgba(124,58,237,0.35) !important;
    border-radius: 18px !important;
    transition: all 0.3s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(124,58,237,0.7) !important;
    background: rgba(255,255,255,0.6) !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.5) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    border-radius: 14px !important;
    color: #374151 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    border-radius: 16px !important;
    margin-bottom: 10px !important;
}

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
    border-radius: 14px !important;
    color: #4a3f6b !important;
    font-weight: 600 !important;
}

.result-glass {
    background: rgba(255,255,255,0.45);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 8px 32px rgba(120,80,200,0.1);
    margin-top: 20px;
    animation: fadeIn 0.5s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hist-card {
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: all 0.25s ease;
}
.hist-card:hover {
    background: rgba(255,255,255,0.55);
    transform: translateX(6px);
    box-shadow: 0 4px 20px rgba(124,58,237,0.12);
}

.empty-state {
    text-align: center;
    padding: 64px 20px;
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    border: 1px dashed rgba(124,58,237,0.2);
    border-radius: 20px;
    margin-top: 12px;
}
.empty-icon { font-size: 3.5rem; margin-bottom: 14px; animation: bounce 2s ease-in-out infinite; }
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.empty-title { font-weight: 700; font-size: 1.1rem; color: #7c3aed; margin-bottom: 6px; }
.empty-sub { font-size: 0.85rem; color: #9ca3af; }

.chip {
    display: inline-block;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #6d28d9;
    margin: 3px;
}

.stMarkdown h1,.stMarkdown h2,.stMarkdown h3 {
    color: #4c1d95 !important;
    font-weight: 700 !important;
}
.stMarkdown p, .stMarkdown li { color: #374151 !important; line-height: 1.75 !important; }
.stMarkdown strong { color: #5b21b6 !important; }
hr { border-color: rgba(124,58,237,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-date">✦ {bugun}</div>
    <p class="hero-title">CV Kariyer<br>Asistanı</p>
    <p class="hero-sub">Yapay zeka ile CV'nizi analiz edin, güçlü yönlerinizi keşfedin, kariyerinizi şekillendirin.</p>
</div>
""", unsafe_allow_html=True)

# ── STAT KARTLARI ────────────────────────────────────────────────
gecmis = gecmis_analizleri_getir()

st.markdown(f"""
<div class="stat-row">
    <div class="stat-glass">
        <div class="stat-num">{len(gecmis)}</div>
        <div class="stat-lbl">Analiz</div>
    </div>
    <div class="stat-glass">
        <div class="stat-num" style="font-size:1.2rem;padding-top:6px;">
            {"✓" if "cv_adi" in st.session_state else "—"}
        </div>
        <div class="stat-lbl">Aktif CV</div>
    </div>
    <div class="stat-glass">
        <div class="stat-num" style="font-size:1.1rem;padding-top:6px;">2.5</div>
        <div class="stat-lbl">Gemini Flash</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 20px 0;">
        <span style="font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700;
        background:linear-gradient(135deg,#7c3aed,#2563eb);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;background-clip:text;">✨ CV Asistan</span>
    </div>
    """, unsafe_allow_html=True)

    if "cv_adi" in st.session_state:
        st.markdown(f"""
        <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.25);
        border-radius:12px;padding:12px 14px;margin-bottom:16px;">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:1px;
            text-transform:uppercase;color:#9ca3af;margin-bottom:4px;">Aktif CV</div>
            <div style="font-size:0.85rem;font-weight:600;color:#6d28d9;">
                📄 {st.session_state['cv_adi']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#9ca3af;margin-bottom:10px;">Desteklenen Formatlar</div>', unsafe_allow_html=True)
    st.markdown('<span class="chip">📄 PDF</span><span class="chip">📝 DOCX</span>', unsafe_allow_html=True)

    st.divider()

    st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#9ca3af;margin:16px 0 10px 0;">Son Analizler</div>', unsafe_allow_html=True)

    if gecmis:
        for a in reversed(gecmis[-4:]):
            st.markdown(f"""
            <div class="hist-card">
                <div style="font-size:0.82rem;font-weight:600;color:#5b21b6;">
                    📁 {os.path.basename(a['cv_dosyasi'])}
                </div>
                <div style="font-size:0.72rem;color:#9ca3af;margin-top:3px;">🕐 {a['tarih']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Henüz analiz yapılmadı.")

    st.divider()
    if st.button("🗑️ Hafızayı Temizle", use_container_width=True):
        hafizayi_temizle()
        st.success("Temizlendi!")
        st.rerun()

# ── SEKMELER ─────────────────────────────────────────────────────
sekme1, sekme2, sekme3, sekme4, sekme5, sekme6= st.tabs([
    "✨ CV Analizi",
    "🗺️ Kariyer Yolu",
    "🎓 Kurs Önerileri",
    "🎯 ATS Skoru",
    "💬 Sohbet",
    "📜 Geçmiş"
])

with sekme1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1,1], gap="large")
    with col1:
        st.markdown("**📂 CV Dosyanızı Yükleyin**")
        yuklenen = st.file_uploader("PDF veya DOCX", type=["pdf","docx"], label_visibility="collapsed")
        if yuklenen:
            st.success(f"✓ **{yuklenen.name}** hazır!")
    with col2:
        st.markdown("**📋 İş İlanı** *(opsiyonel)*")
        ilan = st.text_area("İlan", placeholder="İş ilanını buraya yapıştırın...", height=130, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if yuklenen:
        col_b, _ = st.columns([1,3])
        with col_b:
            if st.button("🔍 Analiz Başlat", type="primary", use_container_width=True):
                with st.spinner("✨ Analiz yapılıyor..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(yuklenen.name)[1]) as tmp:
                        tmp.write(yuklenen.getvalue())
                        tmp_yolu = tmp.name
                    sonuc = cv_analiz_et(tmp_yolu, ilan)
                    analiz_kaydet(yuklenen.name, sonuc)
                    sohbet_ekle("sistem", f"CV analiz edildi: {yuklenen.name} — {bugun}")
                    st.session_state["son_analiz"] = sonuc
                    st.session_state["cv_metni"] = cv_oku(tmp_yolu)
                    st.session_state["cv_adi"] = yuklenen.name
                    os.unlink(tmp_yolu)
                st.success("✅ Analiz tamamlandı!")
                st.rerun()

    if "son_analiz" in st.session_state:
        st.markdown(f"""
        <div class="result-glass">
            <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
            color:#9ca3af;margin-bottom:18px;">✨ ANALİZ SONUCU — {st.session_state.get('cv_adi','').upper()}</div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state["son_analiz"])
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📄</div>
            <div class="empty-title">CV yükleyin ve analizi başlatın</div>
            <div class="empty-sub">Güçlü yönler, eksikler ve iş ilanı uyumu otomatik analiz edilir</div>
        </div>
        """, unsafe_allow_html=True)

with sekme2:
    if "cv_metni" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🗺️</div>
            <div class="empty-title">Önce CV Analizi sekmesinden CV yükleyin</div>
            <div class="empty-sub">CV yüklendikten sonra kariyer yolu analizi yapılabilir</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
        border-radius:12px;padding:10px 16px;margin-bottom:20px;font-size:0.85rem;color:#6d28d9;font-weight:500;">
            ✓ Aktif CV: <strong>{st.session_state.get('cv_adi','')}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗺️ Kariyer Yolu Analizi")
        st.caption("CV'nizdeki deneyim ve becerilere göre kısa, orta ve uzun vadeli kariyer önerileri sunulur.")

        if st.button("🚀 Kariyer Yolumu Analiz Et", type="primary", use_container_width=True):
            with st.spinner("Kariyer yolu analiz ediliyor..."):
                kariyer = kariyer_yolu_analiz_et(st.session_state["cv_metni"])
                st.session_state["kariyer_sonucu"] = kariyer

        if "kariyer_sonucu" in st.session_state:
            kariyer = st.session_state["kariyer_sonucu"]

            # — Mevcut Durum Kartı —
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #7c3aed;">
                <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;margin-bottom:12px;">ŞU ANKİ DURUM</div>
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                    <div>
                        <div style="font-size:0.75rem;color:#9ca3af;font-weight:600;margin-bottom:4px;">SEVİYE</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#7c3aed;">{kariyer.get('mevcut_seviye','—')}</div>
                    </div>
                    <div>
                        <div style="font-size:0.75rem;color:#9ca3af;font-weight:600;margin-bottom:4px;">ALAN</div>
                        <div style="font-size:1.1rem;font-weight:700;color:#2563eb;">{kariyer.get('mevcut_alan','—')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # — Güçlü Yönler —
            guclu = kariyer.get("guclu_yonler", [])
            if guclu:
                chips = "".join([f'<span class="chip">⭐ {g}</span>' for g in guclu])
                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;margin-bottom:12px;">💪 GÜÇLÜ YÖNLER</div>
                    <div>{chips}</div>
                </div>
                """, unsafe_allow_html=True)

            # — Dönem Kartları —
            donemler = [
                ("kisa_vade",  "🌱 Kısa Vade",  "#10b981"),
                ("orta_vade",  "🚀 Orta Vade",  "#2563eb"),
                ("uzun_vade",  "🏆 Uzun Vade",  "#7c3aed"),
            ]

            cols = st.columns(3)
            for col, (anahtar, baslik, renk) in zip(cols, donemler):
                veri = kariyer.get(anahtar, {})
                sure = veri.get("sure", "")
                pozisyonlar = veri.get("pozisyonlar", [])
                pozisyon_html = "".join([f'<div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.3);font-size:0.85rem;color:#374151;">→ {p}</div>' for p in pozisyonlar])

                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 3px solid {renk};min-height:220px;">
                        <div style="font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:{renk};margin-bottom:6px;">{baslik}</div>
                        <div style="font-size:0.72rem;color:#9ca3af;margin-bottom:14px;">⏱ {sure}</div>
                        <div style="font-size:0.72rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#9ca3af;margin-bottom:8px;">POZİSYONLAR</div>
                        {pozisyon_html if pozisyon_html else '<div style="font-size:0.82rem;color:#d1d5db;">—</div>'}
                    </div>
                    """, unsafe_allow_html=True)

            # — Kişisel Tavsiye —
            tavsiye = kariyer.get("tavsiye", "")
            if tavsiye:
                st.markdown(f"""
                <div class="glass-card" style="border-left:4px solid #f59e0b;background:rgba(245,158,11,0.06);">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;margin-bottom:10px;">💡 KİŞİSEL TAVSİYE</div>
                    <div style="font-size:0.95rem;color:#374151;line-height:1.75;">{tavsiye}</div>
                </div>
                """, unsafe_allow_html=True)

with sekme3:
    if "cv_metni" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎓</div>
            <div class="empty-title">Önce CV Analizi sekmesinden CV yükleyin</div>
            <div class="empty-sub">CV yüklendikten sonra web destekli sertifika ve kurs önerileri oluşturulur</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
        border-radius:12px;padding:10px 16px;margin-bottom:20px;font-size:0.85rem;color:#6d28d9;font-weight:500;">
            ✓ Aktif CV: <strong>{st.session_state.get('cv_adi','')}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎓 Web Destekli Sertifika ve Kurs Önerileri")
        st.caption(
            "Bu bölüm CV'deki eksik/geliştirilebilir becerilere göre web'de "
            "sertifikalı eğitim arar ve kariyer açısından en uygun olanları açıklar."
        )

        if st.button("🌐 Kursları Web'de Ara", type="primary", use_container_width=True):
            with st.spinner("CV'ye göre kurslar aranıyor ve değerlendiriliyor..."):
                kurs_sonucu = sertifika_kurs_oner(st.session_state["cv_metni"])
                st.session_state["kurs_sonucu"] = kurs_sonucu

        if "kurs_sonucu" in st.session_state:
            kurs_sonucu = st.session_state["kurs_sonucu"]

            if kurs_sonucu.get("durum") == "api_yok_veya_sonuc_yok":
                st.warning(kurs_sonucu.get("mesaj", "Web araması yapılamadı."))
                st.info(".env dosyasına TAVILY_API_KEY eklediğinizden emin olun.")

            else:
                st.markdown("#### Genel Değerlendirme")
                st.write(kurs_sonucu.get("genel_degerlendirme", ""))

                oneriler = kurs_sonucu.get("oneriler", [])

                if not oneriler:
                    st.info("Uygun kurs önerisi oluşturulamadı.")

                else:
                    for i, kurs in enumerate(oneriler, start=1):
                        with st.container(border=True):
                            st.markdown(f"### {i}. {kurs.get('kurs_adi', 'Kurs adı yok')}")
                            st.markdown(f"**Platform:** {kurs.get('platform', '-')}")
                            st.markdown(f"**Uygunluk:** {kurs.get('uygunluk', '-')}")
                            st.markdown(f"**Hedef beceri:** {kurs.get('hedef_beceri', '-')}")
                            st.markdown(f"**Neden önerildi?** {kurs.get('neden_onerildi', '-')}")
                            st.markdown(f"**CV'ye katkısı:** {kurs.get('cvye_katkisi', '-')}")

                            link = kurs.get("link", "")

                            if link:
                                st.link_button("Kursa Git", link)
with sekme4:
    if "cv_metni" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎯</div>
            <div class="empty-title">Önce CV Analizi sekmesinden CV yükleyin</div>
            <div class="empty-sub">CV yüklendikten sonra ATS uyum analizi yapılabilir</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
        border-radius:12px;padding:10px 16px;margin-bottom:20px;font-size:0.85rem;color:#6d28d9;font-weight:500;">
            ✓ Aktif CV: <strong>{st.session_state.get('cv_adi','')}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 ATS Uyum Analizi")
        st.caption("CV'nizin bir iş ilanıyla ne kadar örtüştüğünü ATS (Applicant Tracking System) açısından analiz eder.")

        ilan_ats = st.text_area(
            "İş İlanı",
            placeholder="Başvurmak istediğiniz iş ilanını buraya yapıştırın...",
            height=150,
            label_visibility="collapsed",
            key="ilan_ats"
        )

        if st.button("🎯 ATS Analizi Başlat", type="primary", use_container_width=True):
            if not ilan_ats.strip():
                st.warning("⚠️ Lütfen bir iş ilanı girin.")
            else:
                with st.spinner("ATS analizi yapılıyor..."):
                    ats = ats_analiz_et(st.session_state["cv_metni"], ilan_ats)
                    st.session_state["ats_sonucu"] = ats

        if "ats_sonucu" in st.session_state:
            ats = st.session_state["ats_sonucu"]
            skor = ats.get("ats_skoru", 0)

            # Skora göre renk
            if skor >= 70:
                renk = "#10b981"
                etiket = "Güçlü Uyum ✓"
            elif skor >= 40:
                renk = "#f59e0b"
                etiket = "Orta Uyum ⚡"
            else:
                renk = "#ef4444"
                etiket = "Zayıf Uyum ✗"

            # — Skor Kartı —
            st.markdown(f"""
            <div class="glass-card" style="border-top:4px solid {renk};text-align:center;padding:36px;">
                <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                color:#9ca3af;margin-bottom:16px;">ATS UYUM SKORU</div>
                <div style="font-family:'Playfair Display',serif;font-size:5rem;font-weight:800;
                color:{renk};line-height:1;">{skor}</div>
                <div style="font-size:0.85rem;font-weight:600;color:{renk};margin-top:8px;">{etiket}</div>
                <div style="margin-top:20px;background:rgba(0,0,0,0.06);border-radius:99px;height:10px;">
                    <div style="width:{skor}%;background:{renk};height:10px;border-radius:99px;
                    transition:width 1s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # — Özet —
            ozet = ats.get("ozet", "")
            if ozet:
                st.markdown(f"""
                <div class="glass-card" style="border-left:4px solid {renk};">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                    color:#9ca3af;margin-bottom:10px;">📋 GENEL DEĞERLENDİRME</div>
                    <div style="font-size:0.95rem;color:#374151;line-height:1.75;">{ozet}</div>
                </div>
                """, unsafe_allow_html=True)

            # — Keyword'ler —
            col_a, col_b = st.columns(2)

            with col_a:
                eslesen = ats.get("eslesen_keywords", [])
                chips_eslesen = "".join([f'<span class="chip" style="background:rgba(16,185,129,0.12);border-color:rgba(16,185,129,0.3);color:#065f46;">✓ {k}</span>' for k in eslesen])
                st.markdown(f"""
                <div class="glass-card" style="border-top:3px solid #10b981;">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                    color:#9ca3af;margin-bottom:12px;">✅ EŞLEŞEN KEYWORD'LER ({len(eslesen)})</div>
                    <div>{chips_eslesen if chips_eslesen else '<span style="color:#d1d5db;font-size:0.85rem;">Eşleşen keyword bulunamadı</span>'}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                eksik = ats.get("eksik_keywords", [])
                chips_eksik = "".join([f'<span class="chip" style="background:rgba(239,68,68,0.1);border-color:rgba(239,68,68,0.25);color:#991b1b;">✗ {k}</span>' for k in eksik])
                st.markdown(f"""
                <div class="glass-card" style="border-top:3px solid #ef4444;">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                    color:#9ca3af;margin-bottom:12px;">❌ EKSİK KEYWORD'LER ({len(eksik)})</div>
                    <div>{chips_eksik if chips_eksik else '<span style="color:#d1d5db;font-size:0.85rem;">Tüm keyword\'ler mevcut!</span>'}</div>
                </div>
                """, unsafe_allow_html=True)

            # — Öneriler —
            oneriler = ats.get("oneriler", [])
            if oneriler:
                st.markdown(f"""
                <div class="glass-card" style="border-left:4px solid #f59e0b;background:rgba(245,158,11,0.04);">
                    <div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
                    color:#9ca3af;margin-bottom:16px;">💡 İYİLEŞTİRME ÖNERİLERİ</div>
                    {''.join([f"""<div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.4);">
                        <div style="min-width:24px;height:24px;background:rgba(245,158,11,0.15);border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:0.75rem;
                        font-weight:700;color:#d97706;">{i+1}</div>
                        <div style="font-size:0.88rem;color:#374151;line-height:1.6;">{o}</div>
                    </div>""" for i, o in enumerate(oneriler)])}
                </div>
                """, unsafe_allow_html=True)

with sekme5:
    if "cv_metni" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">💬</div>
            <div class="empty-title">Önce CV Analizi sekmesinden CV yükleyin</div>
            <div class="empty-sub">CV yüklendikten sonra soru sorabilirsiniz</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);
        border-radius:12px;padding:10px 16px;margin-bottom:20px;font-size:0.85rem;color:#6d28d9;font-weight:500;">
            ✓ Aktif CV: <strong>{st.session_state.get('cv_adi','')}</strong>
        </div>
        """, unsafe_allow_html=True)

        if "mesajlar" not in st.session_state:
            st.session_state["mesajlar"] = []

        for m in st.session_state["mesajlar"]:
            with st.chat_message(m["rol"]):
                st.markdown(m["icerik"])

        soru = st.chat_input("Sorunuzu yazın... (örn: 'Hangi beceriler eksik?')")
        if soru:
            st.session_state["mesajlar"].append({"rol":"user","icerik":soru})
            sohbet_ekle("kullanici", soru)
            with st.chat_message("user"):
                st.markdown(soru)
            with st.chat_message("assistant"):
                with st.spinner("Düşünüyor..."):
                    cevap = soru_sor(st.session_state["cv_metni"], soru)
                st.markdown(cevap)
            st.session_state["mesajlar"].append({"rol":"assistant","icerik":cevap})
            sohbet_ekle("asistan", cevap)

with sekme6:
    gecmis = gecmis_analizleri_getir()
    if not gecmis:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📜</div>
            <div class="empty-title">Henüz analiz yapılmadı</div>
            <div class="empty-sub">İlk analizini yaptıktan sonra burada görünecek</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;margin-bottom:20px;">✨ {len(gecmis)} ANALİZ KAYDI</div>', unsafe_allow_html=True)
        for a in reversed(gecmis):
            with st.expander(f"📁 {a['cv_dosyasi']}  ·  {a['tarih']}"):
                st.markdown(a["sonuc"])