import streamlit as st
import pandas as pd
import os

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil za tamnu temu i široko plavo dugme
st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:4px;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#279FF5!important; border:none!important; width:100%!important; text-shadow:none!important; height: 45px!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#279FF5!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;}</style>", unsafe_allow_html=True)

# Inicijalizacija session_state liste za tabelu
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Izbor jezika na vrhu aplikacije
jezik = st.selectbox("🌐 Jezik / Language / Idioma / Sprache", ["Srpski", "English", "Español", "Deutsch"])

# --- REČNIK TEKSTOVA ZA VIŠEJEZIČNOST ---
if jezik == "English":
    t_naslov = "♠️♥️Diet Diary♦️♣️"
    t_podnaslov = "mineral levels tracking with daily intake sum"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg*"
    t_korak1 = "🔍 Step 1: Search for a food item from the database"
    t_input1 = "Enter food name to search:"
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
    t_labela_unos = "Amount in grams"
    t_default_pretraga = "coffee" # Podrazumevana reč za engleski
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
    t_labela_unos = "Cantidad en gramos"
    t_default_pretraga = "café" # Podrazumevana reč za španski
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
    t_labela_unos = "Menge in Gramm"
    t_default_pretraga = "kaffee" # Podrazumevana reč za nemački
else:
    t_naslov = "♠️♥️Dnevnik Ishrane♦️♣️"
    t_podnaslov = "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu iz baze podataka"
    t_input1 = "Unesite naziv namirnice za pretragu:"
    t_korak2 = "🔍 Korak 2: Izaberite namirnicu sa liste:"
    t_okvir = "Vrednosti na 100g -> Kalijum: {} mg | Fosfor: {} mg | Natrijum: {} mg"
    t_korak3 = "⚖️ Korak 3: Upišite količinu namirnice u gramima"
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
    t_labela_unos = "Količina u gramima"
    t_default_pretraga = "kafa" # Podrazumevana reč za srpski

# Prikaz zaglavlja aplikacije
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}<br><span style='font-size: 22px; font-weight: normal;'>{t_podnaslov}</span></h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df_baza = pd.read_excel("KPH-AI.xlsx")
        df_baza.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df_baza
    except:
        return None

df = ucitaj_bazu()

# --- LOGIČKE FUNKCIJE ZA DUGMAD ---
def dodaj_obrok_callback():
    if 'trenutni_izbor' in st.session_state and 'trenutna_kolicina' in st.session_state:
        odabrana_hrana = st.session_state['trenutni_izbor']
        kolicina = float(st.session_state['trenutna_kolicina'])
        
        red = df[df[ime_kolone_baza] == odabrana_hrana]
        if not red.empty:
            k = float(red['Kalijum'].values[0])
            f = float(red['Fosfor'].values[0])
            n = float(red['Natrijum'].values[0])
            
            st.session_state['dnevnik_obroka'].append({
                col_namirnica: odabrana_hrana,
                col_kolicina: kolicina,
                col_kalijum: round((k * kolicina) / 100.0, 2),
                col_fosfor: round((f * kolicina) / 100.0, 2),
                col_natrijum: round((n * kolicina) / 100.0, 2)
            })

def isprazni_dnevnik_callback():
    st.session_state['dnevnik_obroka'] = []

# --- GLAVNI RENDER STRANICE ---
if df is not None:
    st.write("---")
    st.subheader(t_korak1)
    
    # DODATO: polje sada ima 'value=t_default_pretraga' što postavlja 'kafa' kao podrazumevanu pretragu na startu
    pretraga = st.text_input(t_input1, value=t_default_pretraga, key="polje_pretrage")
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
        izbor = st.selectbox("Izaberi stavku:", lista_za_selectbox, label_visibility="collapsed", key="trenutni_izbor")
        
        trenutni_red = df[df[ime_kolone_baza] == izbor]
        if not trenutni_red.empty:
            k_100 = trenutni_red['Kalijum'].values[0]
            f_100 = trenutni_red['Fosfor'].values[0]
            n_100 = trenutni_red['Natrijum'].values[0]
