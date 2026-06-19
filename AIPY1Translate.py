import streamlit as st
import pandas as pd

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil za tamnu temu i široko plavo dugme preko celog ekrana
st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:4px;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#279FF5!important; border:none!important; width:100%!important; text-shadow:none!important; height: 45px!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#279FF5!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;}</style>", unsafe_allow_html=True)

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
    t_napomena2 = "ⓘ *Recommended daily intake: Potassium 1200-1500mg | Phosphorus 800-1000mg*"
    t_korak1 = "🔍 Step 1: Click and type a letter to find food (A-Z sorted):"
    t_okvir = "Values per 100g -> Potassium: {} mg | Phosphorus: {} mg | Sodium: {} mg"
    t_korak2 = "⚖️ Step 2: Enter the amount of food consumed (in grams):"
    t_dugme_dodaj = "➕ Add meal to my diary"
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
    ime_kolone_baza = 'Namirnica_EN'
    t_labela_unos = "Amount in grams"
elif jezik == "Español":
    t_naslov, t_podnaslov = "♠️♥️Diario de Alimentación♦️♣️", "seguimiento de minerales con suma de ingesta diaria"
    t_napomena1 = "⚠️ *Los valores de minerales se expresan in miligramos (mg) por cada 100 gramos de alimento limpio y crudo.*"
    t_napomena2 = "ⓘ *Ingesta diaria recomendada: Potasio 1200-1500mg | Fósforo 800-1000mg*"
    t_korak1 = "🔍 Paso 1: Busque un alimento en la lista (Ordenado A-Z):"
    t_okvir = "Valores por 100g -> Potasio: {} mg | Fósforo: {} mg | Sodio: {} mg"
    t_korak2 = "⚖️ Paso 2: Ingrese la cantidad de alimento (en gramos):"
    t_dugme_dodaj = "➕ Añadir comida a mi diario"
    t_naslov_tabele = "📋 Su registro diario de dieta y comidas ingresadas"
    t_zbir_okvir = "📊 SUMA TOTAL DIARIA DE TODAS LAS COMIDAS INGRESADAS:"
    t_dugme_obrisi = "🗑️ Vaciar diario completo"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Alimento', 'Cantidad (g)', 'Potasio (mg)', 'Fósforo (mg)', 'Sodio (mg)'
    ime_kolone_baza = 'Namirnica_ES'
    t_labela_unos = "Cantidad en gramos"
elif jezik == "Deutsch":
    t_naslov, t_podnaslov = "♠️♥️Ernährungstagebuch♦️♣️", "Überwachung des Mineralstoffgehalts mit täglicher Gesamtaufnahme"
    t_napomena1 = "⚠️ *Die Mineralstoffwerte sind in Milligramm (mg) pro 100 Gramm gereinigter, roher Lebensmittel angegeben.*"
    t_napomena2 = "ⓘ *Empfohlene tägliche Aufnahme: Kalium 1200-1500mg | Phosphor 800-1000mg*"
    t_korak1 = "🔍 Schritt 1: Lebensmittel aus der Liste auswählen (A-Z sortiert):"
    t_okvir = "Werte pro 100g -> Kalium: {} mg | Phosphor: {} mg | Natrium: {} mg"
    t_korak2 = "⚖️ Schritt 2: Verzehrte Menge in Gramm eingeben:"
    t_dugme_dodaj = "➕ Mahlzeit hinzufügen"
    t_naslov_tabele = "📋 Ihr tägliches Ernährungsprotokoll und eingegebene Mahlzeiten"
    t_zbir_okvir = "📊 TÄGLICHE GESAMTSUMME ALLER EINGEGEBENEN MAHLZEITEN:"
    t_dugme_obrisi = "🗑️ Tagebuch leeren"
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
    t_labela_unos = "Menge in Gramm"
else:
    t_naslov, t_podnaslov = "♠️♥️Dnevnik Ishrane♦️♣️", "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu (Lista je sortirana po abecedi A-Z)"
    t_okvir = "Vrednosti na 100g -> Kalijum: {} mg | Fosfor: {} mg | Natrijum: {} mg"
    t_korak2 = "⚖️ Korak 2: Upišite količinu namirnice u gramima"
    t_dugme_dodaj = "➕ Dodaj obrok u moj dnevnik"
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    
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

# --- CALLBACK FUNKCIJE SA FIKSNIM ENGLESKIM KLJUČEVIMA ---
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
    st.subheader(t_korak1)
    
    izbor = st.selectbox("👇", kompletna_lista, key="trenutni_izbor", label_visibility="collapsed")
    
    trenutni_red = df[df[ime_kolone_baza] == izbor]
    if not trenutni_red.empty:
        k_100 = trenutni_red['Kalijum'].values[0]
        f_100 = trenutni_red['Fosfor'].values[0]
        n_100 = trenutni_red['Natrijum'].values[0]
        
        # HTML kutija koja forsira prelepu svetlo plavu boju i bezbedna je za telefone
        tekst_za_prikaz = t_okvir.format(k_100, f_100, n_100)
        st.markdown(f"<div style='background-color: #1a2130; padding: 12px; border-left: 4px solid #279FF5; border-radius: 4px; color: #7cd0ff; font-weight: bold; font-size: 15px;'>{tekst_za_prikaz}</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader(t_korak2)
    
    kolicina_g = st.number_input(t_labela_unos, min_value=1.0, max_value=5000.0, value=100.0, step=10.0, label_visibility="collapsed", key="trenutna_kolicina")
    
    st.write("")
    st.button(t_dugme_dodaj, on_click=dodaj_obrok_callback)
        
    # --- PRIKAZ DNEVNIKA ISHRANE ---
    if st.session_state['dnevnik_obroka']:
        st.write("---")
        st.subheader(t_naslov_tabele)
        
        # Pravljenje tabele iz pozadinske liste
        df_prikaz = pd.DataFrame(st.session_state['dnevnik_obroka'])
        
        # Računanje suma preko sigurnih engleskih ključeva
        uk_k = df_prikaz['potassium'].sum()
        uk_f = df_prikaz['phosphorus'].sum()
        uk_n = df_prikaz['sodium'].sum()
        
        # Remapiranje kolona za krajnjeg korisnika
        df_prikaz_prevedeno = df_prikaz.rename(columns={
            'food': l_namirnica,
            'amount': l_kolicina,
            'potassium': l_kalijum,
            'phosphorus': l_fosfor,
            'sodium': l_natrijum
        })
        
        st.dataframe(df_prikaz_prevedeno, use_container_width=True, hide_index=True)
        
        st.write("")
        st.markdown(f"### {t_zbir_okvir}")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label=l_kalijum, value=f"{uk_k:.2f} mg")
        with col_m2:
            st.metric(label=l_fosfor, value=f"{uk_f:.2f} mg")
        with col_m3:
            st.metric(label=l_natrijum, value=f"{uk_n:.2f} mg")
else:
    st.error("Baza podataka 'KPH-AI-GLOBAL.xlsx' nije pronađena ili je oštećena.")

# --- FUTER SA INFORMACIJAMA I BROJAČEM POSETA BEZ RAZMAKA ---
st.write("---")
st.markdown("""
<div style='text-align: center; line-height: 1.2;'>
    <p style='margin: 0px; color: #ffffff; font-size: 14px;'>Ukupno poseta aplikaciji: <span style='color: #279FF5; font-weight: bold;'>3010</span></p>
    <p style='margin: 5px 0px 0px 0px; font-weight: bold; color: #ffffff;'>♣️♦️♥️♠️ MAGICOMP & AI Gemini</p>
    <p style='margin: 0px; color: #279FF5;'>magy@usa.com &nbsp;&nbsp;|&nbsp;&nbsp; Tel.+38163310850</p>
    <p style='margin: 0px;  color: #888888; font-size: 12px;'>Powered by PYTHON</p>
</div>
""", unsafe_allow_html=True)
