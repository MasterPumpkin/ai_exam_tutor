# 🎓 Maturitní AI Trenér programování

Interaktivní webová aplikace pro přípravu na maturitní zkoušku z programování. Využívá AI model **Llama 3.3 70B** přes [Groq API](https://groq.com/) ke generování unikátních zadání a k sokratovskému hodnocení studentských řešení.

## ✨ Funkce

### 1️⃣ Generátor zadání
- Vygeneruje unikátní maturitní úlohu pro zvolený okruh
- Každé zadání má **jasná hodnotící kritéria** s bodovým rozpisem
- Zadání obsahuje skrytá metadata pro automatický evaluátor
- Podporované okruhy:
  - **Imperativní programování** – cykly, funkce, základní algoritmy
  - **Objektově orientované programování** – třídy, dědičnost, zapouzdření
  - **Datové struktury** – slovníky, seznamy, třídění, vyhledávání

### 2️⃣ Evaluátor řešení (Inspektor)
- Sokratovské hodnocení – **nenapíše kód za studenta**, ale klade návodné otázky
- Bodové ohodnocení podle kritérií z vygenerovaného zadání
- Interaktivní chat pro diskuzi nad kódem
- Podpora jednotlivých souborů (`.py`, `.js`, `.php`, `.html`, `.css`, `.cpp`) i **ZIP archivů**
- Export celého protokolu zkoušky do `.md` souboru

## 🚀 Instalace a spuštění

### Předpoklady
- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (doporučeno) nebo pip

### 1. Klonování repozitáře
```bash
git clone https://github.com/MasterPumpkin/ai_exam_tutor.git
cd ai_exam_tutor
```

### 2. Instalace závislostí
```bash
# Pomocí uv (doporučeno)
uv sync

# Nebo pomocí pip
pip install -r requirements.txt
```

### 3. Nastavení API klíče
Vytvořte soubor `.env` v kořenu projektu:
```env
GROQ_API_KEY=gsk_váš_klíč_zde
```

> 💡 API klíč získáte zdarma na [console.groq.com/keys](https://console.groq.com/keys)

Alternativně lze klíč zadat přímo v aplikaci přes levý panel.

### 4. Spuštění
```bash
# Pomocí uv
uv run streamlit run main.py

# Nebo přímo
streamlit run main.py
```

Aplikace se otevře na `http://localhost:8501`.

## 📖 Jak používat

### Generování zadání
1. Přejděte na záložku **Generátor zadání**
2. Vyberte maturitní okruh
3. Klikněte na **Vygenerovat unikátní zadání**
4. Stáhněte vygenerovaný `.md` soubor

### Hodnocení řešení
1. Přejděte na záložku **Evaluátor řešení**
2. Nahrajte vygenerované zadání (`.md`)
3. Nahrajte své řešení (kód nebo ZIP)
4. Klikněte na **Zahájit kontrolu a diskuzi**
5. Diskutujte s AI Inspektorem o svém kódu

## 🛠️ Technologie

| Komponenta | Technologie |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| AI Model | Llama 3.3 70B Versatile |
| API | [Groq](https://groq.com/) |
| Jazyk | Python 3.14+ |

## 📁 Struktura projektu

```
ai_exam_tutor/
├── main.py           # Hlavní aplikace
├── pyproject.toml    # Závislosti a konfigurace projektu
├── .env              # API klíč (není v repozitáři)
├── LICENSE           # MIT licence
├── README.md         # Tento soubor
└── requirements.txt  # Závislosti a konfigurace projektu
```

## 📄 Licence

Tento projekt je licencován pod [MIT licencí](LICENSE).

---

Vytvořil **Josef Nuhlíček** • 2026
