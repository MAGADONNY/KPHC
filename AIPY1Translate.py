import streamlit as st
import pandas as pd

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# --- MODERAN GRAFIČKI CSS STIL ---
st.markdown("""
<style>
    /* Pozadina aplikacije i osnovni tekst */
    .stApp {
        background-color: #0e121a;
        color: #f1f3f9;
    }
    
    /* Elegantna polja za unos (Input i Selectbox) */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #171c26 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] input, div[data-baseweb="input"] input:focus {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: #171c26 !important;
    }
    
    /* Gornje glavno dugme sa gradijentom i animacijom */
    div.stButton > button {
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        color: #ffffff !important;
        background: linear-gradient(135deg, #279FF5 0%, #0077c8 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 48px !important;
        box-shadow: 0 4px 15px rgba(39, 159, 245, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(39, 159, 245, 0.4) !important;
        background: linear-gradient(135deg, #3faeff 0%, #0088e6 100%) !important;
    }
    
    /* Labele i naslovi vidljiviji */
    label, div[data-testid='stWidgetLabel'] p {
        color: #cbd5e0 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 5px !important;
    }
    
    /* Stilizovane mini kartice za vrednosti na 100g */
    .mineral-box {
        background-color: #171c26;
        padding: 10px 15px;
        border-radius: 6px;
        border-top: 3px solid #279FF5;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicijalizacija session_state liste za čuvanje unetih obroka
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Izbor jezika na samom vrhu stranice (Kompaktno spakovano)
col_l1, col_l2 = st.columns([2, 1])
with col_l1:
    st.markdown("<p style='margin-top:8px;'>🌐 **Jezik / Language / Idioma / Sprache** (🇷🇸 | 🇬🇧 | 🇪🇸 | 🇩🇪)</p>", unsafe_allow_html=True)
with col_l2:
    jezik = st.selectbox("Izbor jezika", ["Srpski", "English", "Español", "Deutsch"], label_visibility="collapsed")

# --- REČNIK FIKSNIH TEKSTOVA ZA SVE JEZIKE ---
if jezik == "English":
    t_naslov, t_podnaslov = "♠️♥️Diet Diary♦️♣️", "mineral levels tracking with daily intake sum"
    t_napomena1 = "⚠️ *Mineral values are expressed in milligrams (mg) per 100 grams of cleaned, raw food.*"
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg*"
    t_korak1 = "🔍 Step 1: Find food"
    t_okvir_k, t_okvir_f, t_okvir_n = "Potassium", "Phosphorus", "Sodium"
    t_korak2 = "⚖️ Step 2: Amount (grams)"
    t_dugme_dodaj = "➕ Add meal to my diary"
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
    ime_kolone_baza = 'Namirnica_EN'
    t_labela_unos = "Amount in grams"
elif jezik == "Español":
    t_naslov, t_podnaslov = "♠️♥️Diario de Alimentación♦️♣️", "seguimiento de minerales con suma de ingesta diaria"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan in miligramos (mg) por cada 100 gramos de alimento limpio y crudo.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg*"
    t_korak1 = "🔍 Paso 1: Buscar alimento"
    t_okvir_k, t_okvir_f, t_okvir_n = "Potasio", "Fósforo", "Sodio"
    t_korak2 = "⚖️ Paso 2: Cantidad (gramos)"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
    t_labela_unos = "Cantidad en gramos"
elif jezik == "Deutsch":
    t_naslov, t_podnaslov = "♠️♥️Ernährungstagebuch♦️♣️", "Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg*"
    t_korak1 = "🔍 Schritt 1: Lebensmittel wählen"
    t_okvir_k, t_okvir_f, t_okvir_n = "Kalium", "Phosphor", "Natrium"
    t_korak2 = "⚖️ Schritt 2: Menge (Gramm)"
    t_dugme_dodaj = "➕ Mahlzeit hinzufügen"
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_dugme_obrisi = "🗑️ Tagebuch leeren"
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
    t_labela_unos = "Menge in Gramm"
else:
    t_naslov, t_podnaslov = "♠️♥️Dnevnik Ishrane♦️♣️", "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu"
    t_okvir_k, t_okvir_f, t_okvir_n = "Kalijum", "Fosfor", "Natrijum"
    t_korak2 = "⚖️ Korak 2: Upišite gramažu"
    t_dugme_dodaj = "➕ Dodaj obrok u moj dnevnik"
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Namirnica', 'Količina (g)', 'Kalijum (mg)', 'Fosfor (mg)', 'Natrijum (mg)'
    ime_kolone_baza = 'Namirnica'
    t_labela_unos = "Količina u gramima"

# Prikaz naslova aplikacije
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}<br><span style='font-size: 19px; font-weight: normal; color: #a0aec0;'>{t_podnaslov}</span></h1>", unsafe_allow_html=True)

st.info(f"{t_napomena1}\n\n{t_napomena2}")

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    try:
        df_baza = pd.read_excel("KPH-AI-GLOBAL.xlsx")
        df_baza.columns = ['Namirnica', 'Namirnica_EN', 'Namirnica_ES', 'Namirnica_DE', 'Kalijum', 'Fosfor', 'Natrijum']
        return df_baza
    except:
        return None

df = ucitaj_bazu()

# --- CALLBACK FUNKCIJE ---
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
                'food': odabrana_hrana,
                'amount': kolicina,
                'potassium': round((k * kolicina) / 100.0, 2),
                'phosphorus': round((f * kolicina) / 100.0, 2),
                'sodium': round((n * kolicina) / 100.0, 2)
            })

def isprazni_dnevnik_callback():
    st.session_state['dnevnik_obroka'] = []

# --- GLAVNI RENDER STRANICE ---
if df is not None:
    df_sortirano = df.dropna(subset=[ime_kolone_baza]).sort_values(by=ime_kolone_baza)
    kompletna_lista = df_sortirano[ime_kolone_baza].tolist()
    
    st.write("---")
    
    # GRAFIČKA IZMENA: Pakovanje unosa u dve paralelne kolone (štedi prostor)
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        st.markdown(f"**{t_korak1}**")
        izbor = st.selectbox("👇", kompletna_lista, key="trenutni_izbor", label_visibility="collapsed")
        
    with col_input2:
        st.markdown(f"**{t_korak2}**")
        kolicina_g = st.number_input(t_labela_unos, min_value=1.0, max_value=5000.0, value=100.0, step=10.0, label_visibility="collapsed", key="trenutna_kolicina")
    
    # Prikaz vrednosti na 100g u vidu modernih kartica umesto st.info okvira
    trenutni_red = df[df[ime_kolone_baza] == izbor]
    if not trenutni_red.empty:
        k_100 = trenutni_red['Kalijum'].values[0]
        f_100 = trenutni_red['Fosfor'].values[0]
        n_100 = trenutni_red['Natrijum'].values[0]
        
        st.write("")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"<div class='mineral-box'><small>{t_okvir_k} (100g)</small><br><b style='color:#279FF5; font-size:18px;'>{k_100} mg</b></div>", unsafe_allow_html=True)
        with col_c2:
            st.markdown(f"<div class='mineral-box'><small>{t_okvir_f} (100g)</small><br><b style='color:#279FF5; font-size:18px;'>{f_100} mg</b></div>", unsafe_allow_html=True)
        with col_c3:
            st.markdown(f"<div class='mineral-box'><small>{t_okvir_n} (100g)</small><br><b style='color:#279FF5; font-size:18px;'>{n_100} mg</b></div>", unsafe_allow_html=True)

    st.write("")
    st.button(t_dugme_dodaj, on_click=dodaj_obrok_callback)
        
