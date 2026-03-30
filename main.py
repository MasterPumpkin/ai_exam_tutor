import streamlit as st
import os
from dotenv import load_dotenv
import json
from groq import Groq, RateLimitError, AuthenticationError, APIConnectionError, APITimeoutError, BadRequestError
import re
import zipfile
from zipfile import BadZipFile
import random
from streamlit_ace import st_ace

# --- 1. DATABÁZE MATURITNÍCH OKRUHŮ ---
MATURITNI_OKRUHY = {
    "imperativni": {
        "nazev": "Imperativní programování (Cykly, funkce, základní algoritmy)",
        "vzorove_zadani": "Vytvořte konzolovou aplikaci pro evidenci docházky zaměstnanců pomocí imperativního přístupu. Program musí obsahovat hlavní smyčku s interaktivním uživatelským menu. Uživatel bude moci: 1. Přidat záznam (jméno, datum, čas příchodu a odchodu), 2. Odebrat záznam podle data a jména, 3. Vyhledat záznamy podle jména nebo data, 4. Zobrazit celkový přehled. Data uchovávejte ve vhodné základní datové struktuře (např. vícerozměrné pole nebo seznam slovníků/záznamů). Kód musí být logicky rozdělen do vlastních funkcí/podprogramů.",
        "hodnotici_kriteria": {
            "Teorie imperativního programování (proměnné, cykly, podprogramy)": "max. 5 bodů",
            "Návrh řešení (logické rozdělení do funkcí/procedur, volba datových typů)": "max. 25 bodů",
            "Funkčnost: Hlavní smyčka programu a uživatelské menu (přepínač voleb)": "max. 15 bodů",
            "Funkčnost: Přidání a odebrání záznamu (práce s poli/seznamy)": "max. 15 bodů",
            "Funkčnost: Vyhledávání a formátovaný výpis (iterace přes data)": "max. 15 bodů",
            "Uživatelské rozhraní a validace (ošetření nesmyslných vstupů, formát času/data)": "max. 15 bodů",
            "Kvalita kódu (čitelnost, smysluplné názvy proměnných, dekompozice bez použití OOP)": "max. 10 bodů"
        },
        "instrukce_pro_ai": "Generuj novou maturitní úlohu zaměřenou čistě na imperativní programování (zakaž nebo nevyžaduj použití OOP/tříd). Změň doménu, ale STRIKTNĚ ZACHOVEJ úroveň obtížnosti. Nová úloha MUSÍ vyžadovat: 1. Interaktivní konzolové menu běžící v cyklu (např. while), 2. Ukládání složitějších záznamů do základních datových struktur (pole, seznam), 3. Tvorbu vlastních funkcí/procedur pro jednotlivé operace, 4. Validaci vstupů. Hodnotící kritéria ponech beze změny, pouze je případně slovně přizpůsob novému tématu."
    },
    "oop": {
        "nazev": "Objektově orientované programování (OOP)",
        "vzorove_zadani": "Vytvořte objektově orientovanou aplikaci pro správu vozového parku. Aplikace musí obsahovat třídu `Vehicle` (s atributy jako název, typ, rok výroby, spotřeba) a využívat dědičnost pro rozlišení osobních a nákladních vozidel. Dále vytvořte třídu `ServiceRecord` pro evidenci servisních záznamů ke každému vozidlu. Program musí umět vozidla přidávat (s validací vstupních dat, např. roku), vyhledávat je podle typu či roku, evidovat servisní zásahy a zobrazovat celkové statistiky (průměrná spotřeba, počet vozidel). Systém naplňte minimálně 10 testovacími vozidly.",
        "hodnotici_kriteria": {
            "Teorie a OOP principy (správné pochopení objektů)": "max. 5 bodů",
            "Analýza a návrh (třídy, zapouzdření, implementace dědičnosti)": "max. 30 bodů",
            "Funkčnost: Správa objektů a evidence navázaných záznamů": "max. 15 bodů",
            "Funkčnost: Vyhledávání, statistiky a výpočty (průměry atd.)": "max. 15 bodů",
            "Funkčnost: Validace vstupů a naplnění testovacími daty": "max. 15 bodů",
            "Uživatelské rozhraní (přehlednost a intuitivnost ovládání)": "max. 10 bodů",
            "Kvalita kódu (čitelnost, pojmenování proměnných, struktura)": "max. 10 bodů"
        },
        "instrukce_pro_ai": "Generuj novou maturitní úlohu zaměřenou na OOP. Změň téma a doménu, ale STRIKTNĚ ZACHOVEJ stejnou úroveň obtížnosti a technické požadavky. Nová úloha MUSÍ vyžadovat: 1. Hlavní (rodičovskou) třídu, 2. Dědičnost (minimálně 2 podtřídy), 3. Další třídu pro evidenci navázaných záznamů, 4. Validaci uživatelských vstupů, 5. Výpočty statistik a vyhledávání. Hodnotící kritéria ponech beze změny, pouze je případně slovně přizpůsob novému tématu."
    },
    "datove_struktury": {
        "nazev": "Datové struktury (Slovníky, Seznamy a Algoritmy)",
        "vzorove_zadani": "Vytvořte aplikaci pro správu skladových zásob. Aplikace musí umožňovat přidání nového produktu (název, kód, počet kusů, cena), odebrání produktu na základě kódu, vyhledání produktu podle názvu nebo kódu a zobrazení přehledu zásob s možností seřazení (třídění) podle názvu nebo kódu. Pro uložení dat zvolte a implementujte vhodnou datovou strukturu (např. pole, seznam nebo slovník). Program musí pracovat s minimálně 10 testovacími produkty a musí zajišťovat validaci vstupních dat (např. ošetření záporného počtu kusů na skladě nebo chybného datového typu).",
        "hodnotici_kriteria": {
            "Teorie datových struktur (správné pochopení pojmů)": "max. 5 bodů",
            "Analýza a návrh (volba a definice optimální datové struktury pro daný problém)": "max. 25 bodů",
            "Funkčnost: Vložení a odebrání prvků (včetně naplnění 10 testovacími položkami)": "max. 15 bodů",
            "Funkčnost: Vyhledávání prvků (podle dvou různých atributů, např. jména a ID)": "max. 15 bodů",
            "Funkčnost: Třídění a formátovaný výpis dat": "max. 15 bodů",
            "Uživatelské rozhraní a validace vstupů (ošetření chyb)": "max. 15 bodů",
            "Kvalita kódu (čitelnost, pojmenování proměnných, logická struktura bez písemné dokumentace)": "max. 10 bodů"
        },
        "instrukce_pro_ai": "Generuj novou maturitní úlohu zaměřenou na datové struktury a základní algoritmy nad nimi. Změň doménu, ale STRIKTNĚ ZACHOVEJ stejnou úroveň obtížnosti a požadavky. Nová úloha MUSÍ vyžadovat: 1. Volbu a definici kolekce pro uchování položek s více atributy, 2. Funkce pro CRUD operace (přidání a odstranění položky podle unikátního klíče), 3. Vyhledávání podle minimálně dvou různých vlastností, 4. Výpis položek s možností seřazení (třídění), 5. Validaci logických chyb (např. ID musí být unikátní). Hodnotící kritéria ponech beze změny."
    }
}

MAX_RESENI_ZNAKU = 50_000  # Maximální délka řešení v znacích vkládaná do promptu

# --- 2. FUNKCE ---
def vygeneruj_zadani_podle_sablony(klic_okruhu, api_key, token_placeholder=None):
    sablona = MATURITNI_OKRUHY[klic_okruhu]
    
    system_prompt = f"""Jsi asistent pro tvorbu maturitních úloh z programování.
Tvá role je vygenerovat NOVOU úlohu na základě poskytnutého vzoru a instrukcí.

ZDE JE VZOROVÁ ÚLOHA: {sablona['vzorove_zadani']}
ZDE JSOU POŽADOVANÁ HODNOTÍCÍ KRITÉRIA: {json.dumps(sablona['hodnotici_kriteria'], ensure_ascii=False)}
TVÉ INSTRUKCE K NOVÉ ÚLOZE: {sablona['instrukce_pro_ai']}

VYTVOŘ NOVOU ÚLOHU, KTERÁ BUDE STRIKTNĚ TESTOVAT STEJNÉ DOVEDNOSTI A POUŽIJE STEJNOU STRUKTURU HODNOCENÍ.

Vrať POUZE platný formát JSON s následující strukturou:
{{
    "nazev_ulohy": "...",
    "zadani_markdown": "Zde bude text zadání v Markdownu pro studenta. Zahrň do textu i přehlednou Markdown tabulku hodnocení, aby student věděl, za co dostane body.",
    "metadata": {{
            "tema": "{sablona['nazev']}",
            "hodnotici_kriteria": <ZDE VLOŽ PŘESNOU KOPII JSON objektu hodnotících kritérií ze vzoru. NEMĚŇ NÁZVY KLÍČŮ, PONECH CELÉ VĚTY!>,
            "tajny_pokyn_pro_evaluatora": "Zkontroluj logiku a zaměř se přesně na body v hodnotících kritériích."
        }}
}}"""

    try:
        client = Groq(api_key=api_key)
        
        inspirace = ["vesmírná loď", "psí útulek", "středověká krčma", "půjčovna lyží", 
                     "evidence magických lektvarů", "správa ZOO", "kavárna", "autodílna", 
                     "eshop s elektronikou", "botanická zahrada", "farma plná zvířat", 
                     "rockový festival", "závody formulí"]
        nahodne_tema = random.choice(inspirace)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Vygeneruj maturitní úlohu pro okruh: {sablona['nazev']}. ABSOLUTNĚ KRITICKÝ POKYN: Zasaď příběh úlohy do tohoto prostředí: '{nahodne_tema}'. V žádném případě negeneruj evidenci docházky ani knihovnu!"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        if response.usage and response.usage.total_tokens:
            st.session_state['celkove_tokeny'] += response.usage.total_tokens
            if token_placeholder:
                token_placeholder.metric("📊 Spotřebované tokeny", f"{st.session_state['celkove_tokeny']:,}")
        
        if not response.choices:
            return False, "AI nevrátila žádnou odpověď."
        
        raw_content = response.choices[0].message.content
        if not raw_content:
            return False, "AI vrátila prázdnou odpověď. Zkuste vygenerovat zadání znovu."
        raw_content = raw_content.strip()
        
        if raw_content.startswith("```json"):
            raw_content = raw_content.replace("```json", "", 1)
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        raw_content = raw_content.strip()

        try:
            vysledek_json = json.loads(raw_content)
        except json.JSONDecodeError:
            return False, "AI vrátila neplatný formát odpovědi. Zkuste vygenerovat zadání znovu."
        
        nazev = vysledek_json.get("nazev_ulohy", "Maturitní úloha")
        zadani_md = vysledek_json.get("zadani_markdown", "Chyba: Model nevygeneroval text zadání.")
        metadata = vysledek_json.get("metadata", {"chyba": "Metadata nebyla nalezena"})
        
        finalni_md = f"# Maturitní úloha: {nazev}\n\n"
        finalni_md += f"{zadani_md}\n\n"
        
        metadata_string = json.dumps(metadata, ensure_ascii=False)
        start_tag = "<" + "!-- EVAL_METADATA: "
        end_tag = " --" + ">"
        finalni_md += f"{start_tag}{metadata_string}{end_tag}"
        
        return True, finalni_md
        
    except RateLimitError:
        return False, "Byl překročen limit požadavků na AI. Počkejte prosím minutu a zkuste to znovu."
    except AuthenticationError:
        return False, "API klíč je neplatný nebo expiroval. Zkontrolujte ho v levém panelu."
    except (APIConnectionError, APITimeoutError):
        return False, "Nepodařilo se spojit se serverem AI. Zkontrolujte připojení k internetu a zkuste to znovu."
    except Exception as e:
        return False, f"Neočekávaná chyba: {e}"

def ziskej_metadata_ze_zadani(text):
    """Bezpečně vytáhne skrytá metadata ze zadání. Používá re.DOTALL a toleruje mezery."""    
    pattern = r"<!-- EVAL_METADATA: (.*?) -->"
    nalez = re.search(pattern, text, re.DOTALL) 
    
    if nalez:
        try:
            return json.loads(nalez.group(1))
        except json.JSONDecodeError:
            return None
    return None

# --- KONFIGURACE A API ---
load_dotenv()
st.set_page_config(page_title="Maturitní AI Trenér", page_icon="🎓", layout="wide")

# Kvůli kompatibilitě se podíváme na GROQ_API_KEY i OPENAI_API_KEY z .env
api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY") 

if 'celkove_tokeny' not in st.session_state:
    st.session_state['celkove_tokeny'] = 0

with st.sidebar:
    st.header("⚙️ Nastavení")
    if not api_key:
        st.warning("Nebyl nalezen lokální API klíč. Prosím, vložte svůj Groq API klíč.")
        api_key = st.text_input("API Klíč", type="password", placeholder="gsk_...").strip()
        if api_key:
            st.success("Klíč vložen! Můžete pokračovat.")
    else:
        st.success("API klíč připraven.")
    
    st.markdown("---")
    st.info("💡 **Kde získat API klíč?**\n1. [console.groq.com](https://console.groq.com/keys)\n2. Přihlaste se\n3. Create API Key")
    
    st.markdown("---")
    token_placeholder = st.empty() 
    token_placeholder.metric("📊 Spotřebované tokeny", f"{st.session_state.get('celkove_tokeny', 0):,}")

# --- HLAVNÍ ROZHRANÍ ---
st.title("🎓 Maturitní AI Trenér programování")

if not api_key:
    st.info("👈 Pro spuštění aplikace vložte API klíč v levém panelu.")
    st.stop()

tab_generator, tab_evaluator = st.tabs(["1️⃣ Generátor zadání", "2️⃣ Evaluátor řešení"])

# --- ZÁLOŽKA 1: GENERÁTOR ---
with tab_generator:
    st.header("Generování maturitní úlohy")
    st.write("Vyber si maturitní okruh a aplikace ti vygeneruje unikátní zadání s jasnými pravidly hodnocení.")
    
    moznosti_okruhu = {k: v["nazev"] for k, v in MATURITNI_OKRUHY.items()}
    vybrany_nazev = st.selectbox("Vyber si okruh:", list(moznosti_okruhu.values()))
    vybrany_klic = [k for k, v in moznosti_okruhu.items() if v == vybrany_nazev][0]
    
    if st.button("Vygenerovat unikátní zadání", type="primary"):
        with st.spinner(f"AI na Groqu právě vymýšlí úlohu pro okruh: {vybrany_nazev}..."):
            uspech, vysledek = vygeneruj_zadani_podle_sablony(vybrany_klic, api_key, token_placeholder)
            
            if not uspech:
                st.error(f"❌ {vysledek}")
            else:
                st.session_state['vygenerovane_zadani'] = vysledek
                st.success("Zadání bylo úspěšně vygenerováno! Nyní si ho stáhni.")
    
    if 'vygenerovane_zadani' in st.session_state:
        st.download_button(
            label="📄 Stáhnout zadání (.md)",
            data=st.session_state['vygenerovane_zadani'],
            file_name="maturitni_zadani.md",
            mime="text/markdown"
        )

# --- ZÁLOŽKA 2: EVALUÁTOR ---
with tab_evaluator:
    st.header("Inspektor – Sokratovské hodnocení")
    
    # 1. Nahrání zadání
    soubor_zadani = st.file_uploader("📄 Nahraj zadání (.md)", type=['md'], key="eval_md")
    
    # Náhled zadání – zobrazíme hned po nahrání, bez čekání na řešení
    if soubor_zadani:
        try:
            nahled_zadani = soubor_zadani.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            nahled_zadani = None
        
        if nahled_zadani:
            with st.expander("📄 Kompletní text maturitního zadání", expanded=False):
                ciste_zadani = re.sub(r"<!-- EVAL_METADATA: (.*?) -->", "", nahled_zadani, flags=re.DOTALL)
                st.markdown(ciste_zadani)
    
    st.divider()
    
    # 2. Vložení řešení (soubor nebo editor)
    zpusob_vlozeni = st.radio(
        "Způsob vložení řešení:",
        ["📁 Nahrát soubor / ZIP", "✏️ Psát kód v editoru"],
        horizontal=True
    )
    
    soubor_reseni = None
    kod_z_editoru = ""
    
    if zpusob_vlozeni == "📁 Nahrát soubor / ZIP":
        soubor_reseni = st.file_uploader(
            "Nahraj své řešení (Kód nebo ZIP)",
            type=['py', 'js', 'php', 'html', 'css', 'cpp', 'cs', 'zip'],
            key="eval_py"
        )
    else:
        # Slovník podporovaných jazyků (Klíč = název pro UI, Hodnota = kód pro Ace editor)
        podporovane_jazyky = {
            "Python": "python",
            "JavaScript": "javascript",
            "PHP": "php",
            "C++ / C": "c_cpp",
            "C#": "csharp",
            "HTML": "html",
            "CSS": "css",
            "Java": "java"
        }
        
        vybrany_nazev_jazyka = st.selectbox(
            "Zvolte programovací jazyk:",
            list(podporovane_jazyky.keys())
        )
        vybrany_kod_jazyka = podporovane_jazyky[vybrany_nazev_jazyka]
        
        st.caption(f"✏️ Pište nebo vložte svůj kód v jazyce {vybrany_nazev_jazyka}")
        with st.container(border=True):
            kod_z_editoru = st_ace(
                value="",
                language=vybrany_kod_jazyka,
                theme="github",
                keybinding="vscode",
                font_size=14,
                tab_size=4,
                min_lines=20,
                key="ace_editor"
            )

    # 2. Zpracování souborů / editoru do Cache
    ma_reseni = soubor_reseni or (kod_z_editoru and kod_z_editoru.strip())
    
    if soubor_zadani and ma_reseni:
        
        # Vytvoříme unikátní identifikátor – zvlášť pro zadání a řešení
        zadani_otisk = f"{soubor_zadani.name}_{soubor_zadani.size}"
        
        if zpusob_vlozeni == "📁 Nahrát soubor / ZIP" and soubor_reseni:
            reseni_otisk = f"file_{soubor_reseni.name}_{soubor_reseni.size}"
        else:
            # Hash z textu v editoru – při jakékoli změně kódu se chat resetuje
            reseni_otisk = f"editor_{hash(kod_z_editoru)}"
        
        aktualni_otisk = f"{zadani_otisk}_{reseni_otisk}"
        
        # Ošetření: Načteme soubory poprvé, nebo když se změní "otisk"
        if 'posledni_otisk_souboru' not in st.session_state or st.session_state['posledni_otisk_souboru'] != aktualni_otisk:
            
            # 1. Zpracování zadání (to je vždy .md)
            try:
                st.session_state['obsah_zadani'] = soubor_zadani.getvalue().decode("utf-8")
            except UnicodeDecodeError:
                st.error("❌ Soubor se zadáním není platný textový soubor (chybné kódování). Použijte soubor v UTF-8.")
                st.stop()
            st.session_state['metadata'] = ziskej_metadata_ze_zadani(st.session_state['obsah_zadani'])
            st.session_state['zadani_name'] = soubor_zadani.name
            
            # 2. Zpracování řešení
            if zpusob_vlozeni == "📁 Nahrát soubor / ZIP" and soubor_reseni:
                # --- Nahrání souboru / ZIP ---
                if soubor_reseni.name.lower().endswith('.zip'):
                    nacteny_kod = ""
                    try:
                        archiv = zipfile.ZipFile(soubor_reseni)
                    except BadZipFile:
                        st.error("❌ Nahraný soubor není platný ZIP archiv.")
                        st.stop()
                    
                    with archiv:
                        for jmeno_souboru in archiv.namelist():
                            # Ignorujeme složky a skryté systémové soubory (jako .DS_Store z Macu)
                            if jmeno_souboru.endswith('/') or '__MACOSX' in jmeno_souboru or jmeno_souboru.startswith('.'):
                                continue
                            
                            try:
                                # Zkusíme soubor přečíst jako text
                                obsah = archiv.read(jmeno_souboru).decode('utf-8')
                                nacteny_kod += f"\n\n==== SOUBOR: {jmeno_souboru} ====\n{obsah}\n"
                                if len(nacteny_kod) > MAX_RESENI_ZNAKU:
                                    st.warning("⚠️ Řešení je příliš velké, načtena pouze část souborů.")
                                    break
                            except UnicodeDecodeError:
                                # Pokud je to obrázek (png/jpg) nebo binárka, přeskočíme ho
                                pass
                            except RuntimeError:
                                # Heslem chráněný soubor v ZIP archivu
                                st.error("❌ ZIP archiv obsahuje soubory chráněné heslem. Nahrajte archiv bez hesla.")
                                st.stop()
                    
                    if not nacteny_kod.strip():
                        st.error("❌ ZIP soubor je prázdný nebo neobsahuje žádné čitelné textové soubory.")
                        st.stop()
                        
                    st.session_state['obsah_reseni'] = nacteny_kod
                else:
                    # Klasický jeden soubor (.py, .js atd.)
                    try:
                        obsah_souboru = soubor_reseni.getvalue().decode("utf-8")
                    except UnicodeDecodeError:
                        st.error("❌ Soubor s řešením není platný textový soubor (chybné kódování). Použijte soubor v UTF-8.")
                        st.stop()
                    
                    if len(obsah_souboru) > MAX_RESENI_ZNAKU:
                        st.warning(f"⚠️ Soubor je velmi velký ({len(obsah_souboru):,} znaků). Bude oříznut na {MAX_RESENI_ZNAKU:,} znaků.")
                        obsah_souboru = obsah_souboru[:MAX_RESENI_ZNAKU]
                    
                    st.session_state['obsah_reseni'] = obsah_souboru
            else:
                # --- Kód z inline editoru ---
                obsah_editoru = kod_z_editoru.strip()
                
                if len(obsah_editoru) > MAX_RESENI_ZNAKU:
                    st.warning(f"⚠️ Kód je velmi dlouhý ({len(obsah_editoru):,} znaků). Bude oříznut na {MAX_RESENI_ZNAKU:,} znaků.")
                    obsah_editoru = obsah_editoru[:MAX_RESENI_ZNAKU]
                
                st.session_state['obsah_reseni'] = obsah_editoru
            
            # Uložíme si nový otisk do paměti
            st.session_state['posledni_otisk_souboru'] = aktualni_otisk
            st.session_state['zadani_nahrano'] = True
            
            # Tvrdý reset chatu a Inspektora, protože se změnily zdrojové soubory!
            st.session_state.pop('evaluace_spustena', None)
            st.session_state.pop('chat_history', None)
        
        metadata = st.session_state.get('metadata')
        obsah_zadani = st.session_state.get('obsah_zadani')
        obsah_reseni = st.session_state.get('obsah_reseni')
        
        # --- KONTROLA METADAT PRO AI (Bez vykreslování tabulky do UI) ---
        if not metadata:
            st.error("❌ V souboru nebyla nalezena skrytá metadata pro Inspektora. Ujistěte se, že používáte soubor vygenerovaný v první záložce.")
            st.stop()

        # --- TLAČÍTKO START ---
        if not obsah_reseni:
            st.warning("⚠️ Nebylo načteno žádné řešení. Nahrajte soubory znovu.")
            st.stop()
        
        if not st.session_state.get('evaluace_spustena'):
            if st.button("Zahájit kontrolu a diskuzi", type="primary"):
                # Sestavení prvotního promptu
                system_prompt = f"""Jsi AI Inspektor u maturity z programování. 
Tvým úkolem je vést studenta k opravě jeho kódu pomocí Sokratovské metody.

ZADÁNÍ A KRITÉRIA:
{obsah_zadani}
METADATA PRO BODOVÁNÍ:
{json.dumps(metadata, ensure_ascii=False)}

KÓD STUDENTA:
{obsah_reseni}

=== TVÁ PRAVIDLA CHOVÁNÍ (ABSOLUTNĚ KRITICKÉ) ===
1. SOKRATOVSKÁ METODA A ZÁKAZ PSANÍ KÓDU: NIKDY, za žádných okolností, neposkytuj studentovi kompletní bloky kódu (např. definice třídy, celé funkce nebo cykly). Tvé poslání je donutit ho přemýšlet. Můžeš ukázat maximálně 1-2 řádky kódu POUZE v případě, že vysvětluješ specifikum jazyka nebo opravuješ banální překlep.
2. SCÉNÁŘ "LÍNÝ STUDENT": Pokud student odpovídá jen "nevím", "???", "jak?", nebo nejeví snahu, NEPIŠ KÓD ZA NĚJ! Odpověz mu např.: "Jsem tu, abych tě navedl, ne abych to napsal za tebe. Zkus napsat alespoň jeden řádek sám, nebo mi řekni, které části přesně nerozumíš."
3. V PRVNÍ ZPRÁVĚ (Hodnocení): 
   - Pozdrav studenta.
   - Proveď ODHAD BODOVÁNÍ podle kritérií (např. Funkčnost: 5/15 - nefunguje vyhledávání).
   - Sečti body a urči známku (100-90: 1, 89-80: 2, 79-65: 3, 64-50: 4, pod 50: 5).
   - Pochval, co je v kódu dobře.
   - Vyber JEDEN největší problém a polož k němu návodnou Sokratovskou otázku.
4. V DALŠÍCH ZPRÁVÁCH (Krok za krokem): Buď stručný, ptej se na logiku. Nezahlť studenta výčtem deseti chyb najednou. Řeš s ním vždy jen jeden problém.
5. AKTUALIZACE BODŮ A TÓN: Pokud student kód úspěšně opraví v chatu, pochval ho a mentálně (či textově) mu aktualizuj bodování. Udržuj profesionální, ale lidský tón. Nepiš jako robot.
"""
                st.session_state['chat_history'] = [{"role": "system", "content": system_prompt}]
                
                # Volání AI pro první zprávu
                with st.spinner("Inspektor připravuje hodnocení..."):
                    try:
                        client = Groq(api_key=api_key)
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=st.session_state['chat_history'],
                            temperature=0.3
                        )
                    except RateLimitError:
                        st.error("⏳ Byl překročen limit požadavků na AI. Počkejte prosím minutu a zkuste to znovu.")
                        del st.session_state['chat_history']
                        st.stop()
                    except AuthenticationError:
                        st.error("🔑 API klíč je neplatný nebo expiroval. Zkontrolujte ho v levém panelu.")
                        del st.session_state['chat_history']
                        st.stop()
                    except BadRequestError:
                        st.error("❌ Požadavek na AI selhal (příliš velká data nebo neplatný formát). Zkuste zkrátit řešení a začít znovu.")
                        del st.session_state['chat_history']
                        st.stop()
                    except (APIConnectionError, APITimeoutError):
                        st.error("🌐 Nepodařilo se spojit se serverem AI. Zkontrolujte připojení k internetu.")
                        del st.session_state['chat_history']
                        st.stop()
                    except Exception as e:
                        st.error(f"❌ Neočekávaná chyba: {e}")
                        del st.session_state['chat_history']
                        st.stop()
                
                if not response.choices:
                    st.error("❌ AI nevrátila žádnou odpověď.")
                    del st.session_state['chat_history']
                    st.stop()
                
                if response.usage and response.usage.total_tokens:
                    st.session_state['celkove_tokeny'] += response.usage.total_tokens
                    token_placeholder.metric("📊 Spotřebované tokeny", f"{st.session_state['celkove_tokeny']:,}")
                
                prvni_odpoved = response.choices[0].message.content
                if not prvni_odpoved:
                    st.error("❌ AI vrátila prázdnou odpověď. Zkuste to znovu.")
                    del st.session_state['chat_history']
                    st.stop()
                
                st.session_state['evaluace_spustena'] = True
                st.session_state['chat_history'].append({"role": "assistant", "content": prvni_odpoved})
                st.rerun()

        # --- VYKRESLENÍ CHATU ---
        if st.session_state.get('evaluace_spustena'):
            st.divider()
            
            col_reset, col_download = st.columns(2)
            
            with col_reset:
                # Tlačítko pro reset vymaže historii a stav spuštění
                if st.button("🔄 Resetovat diskuzi", use_container_width=True):
                    st.session_state.pop('evaluace_spustena', None)
                    st.session_state.pop('chat_history', None)
                    st.rerun()
                    
            with col_download:
                # Dynamické sestavení protokolu z historie
                protokol_text = "# Záznam o maturitní zkoušce\n\n"
                for msg in st.session_state['chat_history']:
                    if msg["role"] == "system": 
                        continue
                    autor = "🧑‍🎓 Student" if msg["role"] == "user" else "🤖 Inspektor"
                    protokol_text += f"### {autor}\n{msg['content']}\n\n---\n"
                
                # Tlačítko pro stažení
                st.download_button(
                    label="💾 Stáhnout protokol (.md)",
                    data=protokol_text,
                    file_name="maturitni_protokol.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            st.divider()
            
            # 1. Zobrazení historie (vyjma systémového promptu)
            for msg in st.session_state['chat_history']:
                if msg["role"] != "system":
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            # 2. Vstup od studenta
            if prompt := st.chat_input("Tvá odpověď nebo opravený kód..."):
                prompt = prompt.strip()
                if not prompt:
                    st.rerun()
                
                # Uložíme dotaz a rovnou ho i tady pro jistotu vypíšeme
                st.session_state['chat_history'].append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Volání API a zobrazení odpovědi Inspektora
                with st.chat_message("assistant"):
                    with st.spinner("Inspektor přemýšlí..."):
                        try:
                            client = Groq(api_key=api_key)
                            response = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=st.session_state['chat_history'],
                                temperature=0.3
                            )
                        except RateLimitError:
                            st.toast("⏳ Limit požadavků překročen. Počkejte chvíli a pošlete znovu.", icon="⏳")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        except AuthenticationError:
                            st.toast("🔑 API klíč je neplatný. Zkontrolujte nastavení.", icon="🔑")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        except BadRequestError:
                            st.toast("💬 Konverzace je příliš dlouhá. Resetujte diskuzi a začněte znovu.", icon="💬")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        except (APIConnectionError, APITimeoutError):
                            st.toast("🌐 Nelze se spojit se serverem. Zkuste to znovu.", icon="🌐")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        except Exception as e:
                            st.toast(f"❌ Chyba: {e}", icon="❌")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        
                        if not response.choices:
                            st.toast("🤔 AI nevrátila odpověď. Zkuste to znovu.", icon="🤔")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        
                        # Přičtení tokenů za tuto zprávu
                        if response.usage and response.usage.total_tokens:
                            st.session_state['celkove_tokeny'] += response.usage.total_tokens
                            token_placeholder.metric("📊 Spotřebované tokeny", f"{st.session_state['celkove_tokeny']:,}")
                            
                        odpoved = response.choices[0].message.content
                        if not odpoved:
                            st.toast("🤔 AI vrátila prázdnou odpověď. Zkuste to znovu.", icon="🤔")
                            st.session_state['chat_history'].pop()
                            st.rerun()
                        
                        st.markdown(odpoved)
                        
                        # Uložení odpovědi do historie
                        st.session_state['chat_history'].append({"role": "assistant", "content": odpoved})
                
                # OPRAVA: Tímto příkazem donutíme aplikaci hned překreslit celou stránku,
                # čímž se bezpečně zobrazí jak historie, tak se znovu otevře textové pole.
                st.rerun()