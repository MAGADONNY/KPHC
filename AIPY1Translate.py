import streamlit as st
import pandas as pd
import os

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil sa povećanim fontovima za pretragu, selectbox i polja
st.markdown("""
<style>
    .stApp {background-color:#0e1117; color:#ffffff;} 
    
    /* Povećan font za unos u polju za pretragu i unos količine */
    div[data-baseweb='input'] input {
        font-size: 20px!important; 
        color:#ffffff!important; 
        -webkit-text-fill-color:#ffffff!important;
    }
    div[data-baseweb='input'] {
        background-color:#1e2430!important; 
        border-radius:4px;
    }
    
    /* Povećan font za nazive namirnica unutar selectbox-a (padajućeg menija) */
    div[data-baseweb='select'] div {
        font-size: 20px!important; 
        color:#ffffff!important;
    }
    
    /* Podešavanje jarkoplavog velikog dugmeta */
    div.stButton > button {
        font-weight: 900!important; 
        font-family: sans-serif!important; 
        color: #000000!important; 
        background-color: #279FF5!important; 
        border: none!important; 
        width: 100%!important; 
        text-shadow: none!important; 
        height: 50px!important;
        font-size: 18px!important;
    }
    div.stButton > button:focus, div.stButton > button:active {
        color:#000000!important; 
        background-color:#279FF5!important; 
        font-weight:900!important;
    }
    
    /* Povećan font za glavne labele i naslove koraka */
    label, div[data-testid='stWidgetLabel'] p {
        color:#ffffff!important; 
        font-weight:bold!important; 
        font-size: 18px!important;
    }
</style>
""", unsafe_allow_html=True)

# Jednostavan i bezbedan izbor jezika na samom vrhu stranice
jezik = st.selectbox("🌐 Jezik / Language / Idioma / Sprache", ["Srpski", "English", "Español", "Deutsch"])

# --- REČNIK FIKSNIH TEKSTOVA ZA SVE JEZIKE ---
if jezik == "English":
    t_naslov = "♠️♥️Diet Diary♦️♣️"
    t_podnaslov = "mineral levels tracking with daily intake sum"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg*"
    t_korak1 = "🔍 Step 1: Search for a food item from the database"
    t_input1 = "Enter food name to search (e.g., meat, chicken, beer...):"
    t_korak2 = "🔍 Step 2: Select food from the list:"
    t_okvir = "Values per 100g -> Potassium: {} mg | Phosphorus: {} mg | Sodium: {} mg"
    t_korak3 = "⚖️ Step 3: Enter the amount of food consumed (in grams):"
    t_dugme_dodaj = "➕ Add meal to my diary"
    t_toast = "Added to diary: {} ({}g)"
    t_upozorenje = "No food items match your search. Showing full list."
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_ukupno_k = "Total Potassium: {:.2f} mg"
    t_ukupno_f = "Total Phosphorus: {:.2f} mg"
    t_ukupno_n = "Total Sodium: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
    ime_kolone_baza = 'Namirnica_EN'
elif jezik == "Español":
    t_naslov = "♠️♥️Diario de Alimentación♦️♣️"
    t_podnaslov = "seguimiento de minerales con suma de ingesta diaria"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan en miligramos (mg) por cada 100 gramos de alimento limpio y crudo.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg*"
    t_korak1 = "🔍 Paso 1: Buscar un alimento en la base de datos"
    t_input1 = "Ingrese el nombre del alimento:"
    t_korak2 = "🔍 Paso 2: Seleccione un alimento de la lista:"
    t_okvir = "Valores por 100g -> Potasio: {} mg | Fósforo: {} mg | Sodio: {} mg"
    t_korak3 = "⚖️ Paso 3: Ingrese la cantidad de alimento (en gramos):"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_toast = "Añadido al diario: {} ({}g)"
    t_upozorenje = "No hay alimentos que coincidan. Mostrando lista completa."
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_ukupno_k = "Potasio Total: {:.2f} mg"
    t_ukupno_f = "Fósforo Total: {:.2f} mg"
    t_ukupno_n = "Sodio Total: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
elif jezik == "Deutsch":
    t_naslov = "♠️♥️Ernährungstagebuch♦️♣️"
    t_podnaslov = "Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg*"
    t_korak1 = "🔍 Schritt 1: Suchen Sie nach einem Lebensmittel"
    t_input1 = "Name des Lebensmittels eingeben:"
    t_korak2 = "🔍 Schritt 2: Lebensmittel aus der Liste auswählen:"
    t_okvir = "Werte pro 100g -> Kalium: {} mg | Phosphor: {} mg | Natrium: {} mg"
    t_korak3 = "⚖️ Schritt 3: Verzehrte Menge in Gramm eingeben:"
    t_dugme_dodaj = "➕ Mahlzeit hinzufügen"
    t_toast = "Zum Tagebuch hinzugefügt: {} ({}g)"
    t_upozorenje = "Keine Treffer. Vollständige Liste wird angezeigt."
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_ukupno_k = "Kalium Gesamt: {:.2f} mg"
    t_ukupno_f = "Phosphor Gesamt: {:.2f} mg"
    t_ukupno_n = "Natrium Gesamt: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Tagebuch leeren"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
else:
    t_naslov = "♠️♥️Dnevnik Ishrane♦️♣️"
    t_podnaslov = "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu iz baze podataka"
    t_input1 = "Unesite naziv namirnice za pretragu:"
    t_korak2 = "🔍 Korak 2: Izaberite namirnicu sa liste:"
    t_okvir = "Vrednosti na 100g -> Kalijum: {} mg | Fosfor: {} mg | Natrijum: {} mg"
    t_korak3 = "⚖️ Korak 3: Upišite količinu namirnice u gramima (g):"
    t_dugme_dodaj = "➕ Dodaj obrok u moj dnevnik"
    t_toast = "Dodato u dnevnik: {} ({}g)"
    t_upozorenje = "Nijedna namirnica ne odgovara pretrazi. Prikazujemo celu listu."
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_ukupno_k = "Ukupno Kalijum: {:.2f} mg"
    t_ukupno_f = "Ukupno Fosfor: {:.2f} mg"
    t_ukupno_n = "Ukupno Natrijum: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Namirnica', 'Količina (g)', 'Kalijum (mg)', 'Fosfor (mg)', 'Natrijum (mg)'
    ime_kolone_baza = 'Namirnica'

# Prikaz naslova
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}<br><span style='font-size: 22px; font-weight: normal;'>{t_podnaslov}</span></h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df = pd.read_excel("KPH-AI-GLOBAL.xlsx")
        df.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    st.write("---")
    st.subheader(t_korak1)
    pretraga = st.text_input(t_input1, key="polje_pretrage")
    pojam_za_filter = pretraga.strip()
    
    if pojam_za_filter:
        filtrirano = df[df[ime_kolone_baza].astype(str).str.contains(pojam_za_filter, case=False, na=False)]
        if filtrirano.empty:
            st.warning(t_upozorenje)
            filtrirano = df
    else:
        filtrirano = df

    st.write("---")
    st.subheader(t_korak2)
    
    lista_za_selectbox = filtrirano[ime_kolone_baza].dropna().tolist()
    
    if lista_za_selectbox:
        izbor = st.selectbox("👇", lista_za_selectbox, label_visibility="collapsed")
        red_df = df[df[ime_kolone_baza] == izbor]
        
        if not red_df.empty:
            k_v = pd.to_numeric(red_df['Kalijum'].values[0], errors='coerce')
            k_v = 0.0 if pd.isna(k_v) else float(k_v)
            
            f_v = pd.to_numeric(red_df['Fosfor'].values[0], errors='coerce')
            f_v = 0.0 if pd.isna(f_v) else float(f_v)
            
            n_v = pd.to_numeric(red_df['Natrijum'].values[0], errors='coerce')
            n_v = 0.0 if pd.isna(n_v) else float(n_v)
            
            if k_v > 200: k_boja = "#ff4b4b"
            elif k_v < 100: k_boja = "#00ffcc"
            else: k_boja = "#ffffff"
                
            st.markdown(
                f"""
                <div style='background-color: #1e2430; padding: 15px; border-radius: 5px; border-left: 5px solid {k_boja}; font-size: 19px; font-weight: bold;'>
                    {t_okvir.format(f"<span style='color: {k_boja}; font-weight: bold;'>{k_v}</span>", f_v, n_v)}
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.write("---")
            st.subheader(t_korak3)
