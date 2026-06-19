import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import io

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil za tamnu temu, ZELENO DUGME i prostor za futer na telefonima
st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;padding-bottom:200px!important;} footer {visibility: hidden!important;} [data-testid='stActionButton'] {display: none!important;} [data-testid='stStatusWidget'] {display: none!important;} div[data-baseweb='select'] font-size:18px!important; font-weight:bold!important;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:6px!important; height:50px!important;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important; font-size:18px!important; font-weight:bold!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#2ECC71!important; border:none!important; width:100%!important; text-shadow:none!important; padding: 12px 0px!important; font-size:18px!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#2ECC71!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;} .stSelectbox div[data-baseweb='select'] {font-size:18px!important; font-weight:bold!important; color:#ffffff!important;}</style>", unsafe_allow_html=True)

# Inicijalizacija session_state liste za čuvanje unetih obroka
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Izbor jezika na samom vrhu stranice
st.markdown("🌐 **Jezik / Language / Idioma / Sprache**<br>🇷🇸 | 🇬🇧 | 🇪🇸 | 🇩🇪", unsafe_allow_html=True)
jezik = st.selectbox("Izbor jezika", ["Srpski", "English", "Español", "Deutsch"], label_visibility="collapsed")

# --- REČNIK FIKSNIH TEKSTOVA ZA SVE JEZIKE ---
if jezik == "English":
    t_naslov, t_podnaslov = "♠️♥️Diet Diary♦️♣️", "mineral levels tracking with daily intake sum"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg | Sodium max 1500-2000mg*"
    t_korak1 = "🔍 Step 1: Click and type a letter to find food (A-Z sorted):"
    t_okvir_baza = "Values per 100g -> "
    t_korak2 = "⚖️ Step 2: Enter the amount of food consumed (in grams):"
    t_dugme_dodaj = "➕ Add meal to my diary"
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    t_dugme_pdf = "📄 Download PDF report"
    t_placeholder_ime = "e.g. John Doe"
    t_labela_ime = "Patient name and surname:"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
    ime_kolone_baza = 'Namirnica_EN'
    t_labela_unos = "Amount in grams"
elif jezik == "Español":
    t_naslov, t_podnaslov = "♠️♥️Diario de Alimentación♦️♣️", "seguimiento de minerales con suma de ingesta diaria"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan in miligramos (mg) por cada 100 gramos de alimento limpio y crudo.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg | Sodio máx 1500-2000mg*"
    t_korak1 = "🔍 Paso 1: Busque un alimento en la lista (Ordenado A-Z):"
    t_okvir_baza = "Valores por 100g -> "
    t_korak2 = "⚖️ Paso 2: Ingrese la cantidad de alimento (en gramos):"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    t_dugme_pdf = "📄 Descargar informe PDF"
    t_placeholder_ime = "por ejemplo, Juan Pérez"
    t_labela_ime = "Nombre y apellido del paciente:"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
    t_labela_unos = "Cantidad en gramos"
elif jezik == "Deutsch":
    t_naslov, t_podnaslov = "♠️♥️Ernährungstagebuch♦️♣️", "Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg | Natrium max 1500-2000mg*"
    t_korak1 = "🔍 Schritt 1: Lebensmittel aus der Liste auswählen (A-Z sortiert):"
    t_okvir_baza = "Werte pro 100g -> "
    t_korak2 = "⚖️ Schritt 2: Verzehrte Menge in Gramm eingeben:"
    t_dugme_dodaj = "➕ Mahlzeit hinzufügen"
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_dugme_obrisi = "🗑️ Tagebuch leeren"
    t_dugme_pdf = "📄 PDF-Bericht herunterladen"
    t_placeholder_ime = "z.B. Max Mustermann"
    t_labela_ime = "Name und Vorname des Patienten:"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
    t_labela_unos = "Menge in Gramm"
else:
    t_naslov, t_podnaslov = "♠️♥️Dnevnik Ishrane♦️♣️", "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg | Natrijum max 1500-2000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu (Lista je sortirana po abecedi A-Z)"
    t_okvir_baza = "Vrednosti na 100g -> "
    t_korak2 = "⚖️ Korak 2: Upišite količinu namirnice u gramima"
    t_dugme_dodaj = "➕ Dodaj obrok u moj dnevnik"
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    t_dugme_pdf = "📄 Preuzmi PDF izveštaj"
    t_placeholder_ime = "npr. Petar Petrović"
    t_labela_ime = "Ime i prezime:"

    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Namirnica', 'Količina (g)', 'Kalijum (mg)', 'Fosfor (mg)', 'Natrijum (mg)'
    ime_kolone_baza = 'Namirnica'
    t_labela_unos = "Količina u gramima"

# Prikaz naslova aplikacije
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}<br><span style='font-size: 22px; font-weight: normal;'>{t_podnaslov}</span></h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df_baza = pd.read_excel("KPH-AI-GLOBAL.xlsx")
        df_baza.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df_baza
    except:
        return None

df = ucitaj_bazu()

# --- FUNKCIJA ZA KREIRANJE PDF-a ---
def generisi_pdf_file(ime_pacijenta, godina_rodjenja, df_podaci, uk_k, uk_f, uk_n):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    
    # 1. Užo zeleno polje na vrhu
    pdf.set_fill_color(46, 204, 113)
    pdf.rect(0, 0, 210, 17, "F")
    
    # Naslov unutar zelene trake
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(180, 7, "DNEVNIK ISHRANE & UNOSA MINERALA", 0, 1, "C")
    
    # Vraćamo tekst na tamno sivu
    pdf.set_text_color(44, 62, 80)
    pdf.ln(5) 
    
    # 2. Blok sa podacima - Siva pozadina pojačana na oko 20%
    pdf.set_fill_color(205, 212, 218) 
    pdf.rect(15, 24, 180, 16, "F")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(120, 6, f" IME I PREZIME / GODINA RODJENJA: {ime_pacijenta.upper()} ({godina_rodjenja})", 0, 0)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(60, 6, f"DATUM: {datetime.now().strftime('%d.%m.%Y.')} ", 0, 1, "R")
    pdf.ln(6)
    
    # 3. Tabela obroka (Zeleno-sivo zaglavlje)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(52, 73, 94) 
    pdf.set_text_color(255, 255, 255) 
    
    pdf.cell(65, 9, " Namirnica", 0, 0, "", True)
    pdf.cell(25, 9, "Kolicina (g)", 0, 0, "C", True)
    pdf.cell(30, 9, "Kalijum (mg)", 0, 0, "C", True)
    pdf.cell(30, 9, "Fosfor (mg)", 0, 0, "C", True)
    pdf.cell(30, 9, "Natrijum (mg)", 0, 1, "C", True)
    
    pdf.set_text_color(44, 62, 80)
    pdf.set_font("Helvetica", size=10)
    
    brojac_reda = 0
    for _, red in df_podaci.iterrows():
        if brojac_reda % 2 == 0:
            pdf.set_fill_color(248, 250, 252) 
            is_fill = True
        else:
            is_fill = False
            
        pdf.cell(65, 8, f" {str(red['food'])[:28]}", "B", 0, "", is_fill)
        pdf.cell(25, 8, f"{red['amount']:.1f} g", "B", 0, "C", is_fill)
        pdf.cell(30, 8, f"{red['potassium']:.1f}", "B", 0, "C", is_fill)
        pdf.cell(30, 8, f"{red['phosphorus']:.1f}", "B", 0, "C", is_fill)
        pdf.cell(30, 8, f"{red['sodium']:.1f}", "B", 1, "C", is_fill)
        brojac_reda += 1
        
    pdf.ln(10)
    
    # 4. Donji rezime u tabeli
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(180, 8, "REZIME UKUPNOG DNEVNOG UNOSA:", 0, 1)
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(230, 235, 240)
    pdf.cell(40, 8, " Mineral", 1, 0, "C", True)
