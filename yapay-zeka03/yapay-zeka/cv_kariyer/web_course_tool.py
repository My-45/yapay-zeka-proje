"""CV'ye göre sertifikalı kurs/eğitim arayan basit web arama aracı.

Tavily API kullanır. .env içine şunu ekleyin:
TAVILY_API_KEY="..."
"""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_URL = "https://api.tavily.com/search"


def tavily_ara(sorgu: str, max_sonuc: int = 5) -> list[dict[str, str]]:
    
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key or api_key == "****":
        return []

    payload: dict[str, Any] = {
        "api_key": api_key,
        "query": sorgu,
        "search_depth": "basic",
        "max_results": max_sonuc,
        "include_answer": False,
        "include_raw_content": False,
    }

    try:
        response = requests.post(TAVILY_URL, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    temiz_sonuclar: list[dict[str, str]] = []

    for item in data.get("results", []):
        temiz_sonuclar.append(
            {
                "baslik": item.get("title", "Başlık yok"),
                "link": item.get("url", ""),
                "ozet": item.get("content", ""),
            }
        )

    return temiz_sonuclar


def kurs_sorgulari_olustur(kariyer_json: dict, adet: int = 6) -> list[str]:
    
    alan = kariyer_json.get("mevcut_alan", "kariyer")

    beceriler: list[str] = []

    for bolum in ["kisa_vade", "orta_vade", "uzun_vade"]:
        veri = kariyer_json.get(bolum, {})

        if isinstance(veri, dict):
            beceriler.extend(veri.get("gelismesi_gerekenler", []))

    temiz_beceriler: list[str] = []

    for beceri in beceriler:
        if beceri and beceri not in temiz_beceriler:
            temiz_beceriler.append(beceri)

    if not temiz_beceriler:
        temiz_beceriler = [alan]

    platformlar = (
        "Coursera OR edX OR Udemy OR Microsoft Learn OR BTK Akademi "
        "OR Google Career Certificates OR IBM SkillsBuild"
    )

    sorgular = []

    for beceri in temiz_beceriler[:adet]:
        sorgular.append(f"{beceri} sertifikalı kurs eğitim {alan} {platformlar}")

    return sorgular


def kurslari_webde_ara(
    kariyer_json: dict,
    sorgu_adedi: int = 5,
    sonuc_adedi: int = 4
) -> list[dict[str, str]]:
    
    tum_sonuclar: list[dict[str, str]] = []
    gorulen_linkler: set[str] = set()

    for sorgu in kurs_sorgulari_olustur(kariyer_json, adet=sorgu_adedi):
        for sonuc in tavily_ara(sorgu, max_sonuc=sonuc_adedi):
            link = sonuc.get("link", "")

            if link and link not in gorulen_linkler:
                sonuc["arama_sorgusu"] = sorgu
                tum_sonuclar.append(sonuc)
                gorulen_linkler.add(link)

    return tum_sonuclar[:12]