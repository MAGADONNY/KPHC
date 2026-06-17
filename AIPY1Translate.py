import streamlit as st
import pandas as pd
import os

# Podešavanje izgleda web stranice
st.set_page_config(page_title="Dnevnik Ishrane / Diet Diary", page_icon="🃏", layout="centered")

st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:4px;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#279FF5!important; border:none!important; width:100%!important; text-shadow:none!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#279FF5!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;}</style>", unsafe_allow_html=True)

# --- 🌐 LOGIKA ZA IZBOR JEZIKA (4 JEZIKA) ---
jezik = st.selectbox("🌐 Izaberite jezik / Select Language / Seleccione idioma / Sprache wählen", ["Srpski", "English", "Español", "Deutsch"])

# --- 📋 REČNIK FIKSNIH TEKSTOVA ZA SVE JEZIKE ---
if jezik == "English":
    t_naslov = "♠️♥️Diet Diary♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>mineral levels tracking with daily intake sum</span>"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food. Levels are determined by AI search of the USDA database.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg*"
    t_korak1 = "🔍 Step 1: Search for a food item from the database"
    t_input1 = "Enter food name to search (e.g., meat, chicken, beer...):"
    t_korak2 = "🔍 Step 2: Click and select food from the list:"
    t_okvir = "Values per 100g -> Potassium: {} mg | Phosphorus: {} mg | Sodium: {} mg"
    t_korak3 = "⚖️ Step 3: Enter the amount of food consumed"
    t_input2 = "Enter amount in grams (g):"
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
    t_naslov = "♠️♥️Diario de Alimentación♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>seguimiento de minerales con suma de ingesta diaria</span>"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan en miligramos (mg) por cada 100 gramos de alimento limpio y crudo. Los niveles se determinan mediante búsqueda de IA en la base de datos de la USDA.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg*"
    t_korak1 = "🔍 Paso 1: Buscar un alimento en la base de datos"
    t_input1 = "Ingrese el nombre del alimento para buscar (ej. carne, pollo, cerveza...):"
    t_korak2 = "🔍 Paso 2: Haga clic y seleccione un alimento de la lista:"
    t_okvir = "Valores por 100g -> Potasio: {} mg | Fósforo: {} mg | Sodio: {} mg"
    t_korak3 = "⚖️ Paso 3: Ingrese la cantidad de alimento consumido"
    t_input2 = "Ingrese la cantidad en gramos (g):"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_toast = "Añadido al diario: {} ({}g)"
    t_upozorenje = "No hay alimentos que coincidan con su búsqueda. Mostrando lista completa."
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_ukupno_k = "Potasio Total: {:.2f} mg"
    t_ukupno_f = "Fósforo Total: {:.2f} mg"
    t_ukupno_n = "Sodio Total: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
elif jezik == "Deutsch":
    t_naslov = "♠️♥️Ernährungstagebuch♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme</span>"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben. Die Werte werden durch KI-Suche in der USDA-Datenbank ermittelt.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg*"
    t_korak1 = "🔍 Schritt 1: Suchen Sie nach einem Lebensmittel in der Datenbank"
    t_input1 = "Geben Sie den Namen des Lebensmittels ein (z. B. Fleisch, Hähnchen, Bier...):"
    t_korak2 = "🔍 Schritt 2: Klicken und wählen Sie Lebensmittel aus der Liste aus:"
    t_okvir = "Werte pro 100g -> Kalium: {} mg | Phosphor: {} mg | Natrium: {} mg"
    t_korak3 = "⚖️ Schritt 3: Geben Sie die verzehrte Menge an Lebensmitteln ein"
    t_input2 = "Menge in Gramm (g) eingeben:"
    t_dugme_dodaj = "➕ Mahlzeit zu meinem Tagebuch hinzufügen"
    t_toast = "Zum Tagebuch hinzugefügt: {} ({}g)"
    t_upozorenje = "Keine Lebensmittel entsprechen Ihrer Suche. Vollständige Liste wird angezeigt."
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_ukupno_k = "Kalium Gesamt: {:.2f} mg"
    t_ukupno_f = "Phosphor Gesamt: {:.2f} mg"
    t_ukupno_n = "Natrium Gesamt: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Vollständiges Tagebuch leeren"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
else: # Srpski
    t_naslov = "♠️♥️Dnevnik Ishrane♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>provera nivoa minerala u namirnicama sa zbirom dnevnog unosa</span>"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice (osim ako nije drugačije naznačeno).* Nivo minerala odredjuje se AI pretragom USDA baze."
    t_napomena2 = "ⓘ *Preporuceni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg *"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu iz baze podataka"
    t_input1 = "Unesite naziv namirnice za pretragu:(npr. meso, piletina, sarma, burek, pivo, spagete...)"
    t_korak2 = "🔍 Korak 2. Klikni i izaberi namirnicu sa liste:"
    t_okvir = "Vrednosti na 100g -> Kalijum: {} mg | Fosfor: {} mg | Natrijum: {} mg"
    t_korak3 = "⚖️ Korak 3: Upisite kolicinu konzumirane namirnice"
    t_input2 = "Unesite kolicinu namirnice u gramima (g):"
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

# Prikaz zaglavlja
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}</h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df = pd.read_excel("KPH-AI.xlsx")
        df.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    st.write("")
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
            red = red_df.iloc[0]
            
            k_v = pd.to_numeric(red['Kalijum'], errors='coerce')
            k_v = 0 if pd.isna(k_v) else k_v
            
            f_v = pd.to_numeric(red['Fosfor'], errors='coerce')
            f_v = 0 if pd.isna(f_v) else f_v
            
            n_v = pd.to_numeric(red['Natrijum'], errors='coerce')
            n_v = 0 if pd.isna(n_v) else n_v
            
            if k_v > 200: k_boja = "#ff4b4b"
            elif k_v < 100: k_boja = "#00ffcc"
            else: k_boja = "#ffffff"
                
            st.markdown(
                f"""
                <div style='background-color: #1e2430; padding: 15px; border-radius: 5px; border-left: 5px solid {k_boja};'>
                    {t_okvir.format(f"<span style='color: {k_boja}; font-weight: bold;'>{k_v}</span>", f_v, n_v)}
                </div>
                """, 
                unsafe_allow_html=True
