import streamlit as st
import pandas as pd

# Osnovna podešavanja aplikacije
st.set_page_config(page_title="Diet Diary / Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Bezbedan CSS stil za tamnu temu, ZELENO DUGME i prostor za futer na telefonima
st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;padding-bottom:200px!important;} footer {visibility: hidden!important;} [data-testid='stActionButton'] {display: none!important;} [data-testid='stStatusWidget'] {display: none!important;} div[data-baseweb='select'] font-size:18px!important; font-weight:bold!important;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:6px!important; height:50px!important;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important; font-size:18px!important; font-weight:bold!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#2ECC71!important; border:none!important; width:100%!important; text-shadow:none!important; padding: 12px 0px!important; font-size:18px!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#2ECC71!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:18px!important;} .stSelectbox div[data-baseweb='select'] {font-size:18px!important; font-weight:bold!important; color:#ffffff!important;}</style>", unsafe_allow_html=True)

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
    
    # Nazivi kolona za prikaz korisniku
    l_namirnica, l_kolicina, l_kalijum, l_fosfor, l_natrijum = 'Lebensmittel', 'Menge (g)', 'Kalium (mg)', 'Phosphor (mg)', 'Natrium (mg)'
    ime_kolone_baza = 'Namirnica_DE'
    t_labela_unos = "Menge in Gramm"
else:
    t_naslov, t_podnaslov = "♠️♥️Dnevnik Ishrane♦️♣️", "provera nivoa minerala u namirnicama sa zbirom dnevnog unosa"
    t_napomena1 = "⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice.*"
    t_napomena2 = "ⓘ *Preporučeni dnevni unos: Kalijum 1200-1500mg | Fosfor 800-1000mg | Natrijum max 1500-2000mg*"
    t_korak1 = "🔍 Korak 1: Izaberite namirnicu (sortirano po abecedi A-Z)"
    t_okvir_baza = "Vrednosti na 100g -> "
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

# --- GLAVNI RENDER STRANICE ---
if df is not None:
    df_sortirano = df.dropna(subset=[ime_kolone_baza]).sort_values(by=ime_kolone_baza)
    kompletna_lista = df_sortirano[ime_kolone_baza].tolist()
    
    st.write("---")
    st.subheader(t_korak1)
    
    izbor = st.selectbox("👇", kompletna_lista, key="trenutni_izbor", label_visibility="collapsed")
    
    trenutni_red = df[df[ime_kolone_baza] == izbor]
    if not trenutni_red.empty:
        k_100 = float(trenutni_red['Kalijum'].values[0])
        f_100 = float(trenutni_red['Fosfor'].values[0])
        n_100 = float(trenutni_red['Natrijum'].values[0])
        
        k_boja = "#FF4B4B" if k_100 > 200.0 else "#2ECC71"
        f_boja = "#FF4B4B" if f_100 > 150.0 else "#2ECC71"
        n_boja = "#FF4B4B" if n_100 > 400.0 else "#2ECC71"
        
        st.markdown(f"""
        <div style='background-color: #1e2430; padding: 12px; border-left: 4px solid #2ECC71; border-radius: 4px; color: #ffffff; font-weight: bold; font-size: 15px;'>
            {t_okvir_baza} 
            <span style='color: {k_boja};'>{l_kalijum}: {k_100:.0f} mg</span> | 
            <span style='color: {f_boja};'>{l_fosfor}: {f_100:.0f} mg</span> | 
            <span style='color: {n_boja};'>{l_natrijum}: {n_100:.0f} mg</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader(t_korak2)
    
    kolicina_g = st.number_input(t_labela_unos, min_value=1.0, max_value=5000.0, value=100.0, step=10.0, label_visibility="collapsed", key="trenutna_kolicina")
    
    st.write("")
    
    # Direktna logika dugmeta bez eksternih callback funkcija radi maksimalne stabilnosti tabele
    if st.button(t_dugme_dodaj):
        red_dodaj = df[df[ime_kolone_baza] == izbor]
        if not red_dodaj.empty:
            k_d = float(red_dodaj['Kalijum'].values[0])
            f_d = float(red_dodaj['Fosfor'].values[0])
            n_d = float(red_dodaj['Natrijum'].values[0])
            
            st.session_state['dnevnik_obroka'].append({
                'food': izbor,
                'amount': kolicina_g,
                'potassium': round((k_d * kolicina_g) / 100.0, 2),
                'phosphorus': round((f_d * kolicina_g) / 100.0, 2),
                'sodium': round((n_d * kolicina_g) / 100.0, 2)
            })
            st.rerun()

    # --- PRIKAZ DNEVNIKA ISHRANE ---
    if st.session_state['dnevnik_obroka']:
        st.write("---")
        st.subheader(t_naslov_tabele)
        
        df_prikaz = pd.DataFrame(st.session_state['dnevnik_obroka'])
        
        uk_k = df_prikaz['potassium'].sum()
        uk_f = df_prikaz['phosphorus'].sum()
        uk_n = df_prikaz['sodium'].sum()
        
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
        
        dnevna_k_boja = "#FF4B4B" if uk_k > 1500.0 else "#2ECC71"
        dnevna_f_boja = "#FF4B4B" if uk_f > 1000.0 else "#2ECC71"
        dnevna_n_boja = "#FF4B4B" if uk_n > 2000.0 else "#2ECC71"
        
               # Prikaz modernih HTML metričkih kartica sa zelenom/crvenom gornjom ivicom (VEĆI I BOLD FONT)
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_k_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 16px; font-weight: bold;'>{l_kalijum}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_k_boja}; font-size: 22px; font-weight: 900;'>{uk_k:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_f_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 16px; font-weight: bold;'>{l_fosfor}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_f_boja}; font-size: 26px; font-weight: 900;'>{uk_f:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div style='background-color: #1e2430; padding: 12px; border-radius: 6px; text-align: center; border-top: 3px solid {dnevna_n_boja};'>
                <p style='margin: 0px; color: #a0aec0; font-size: 16px; font-weight: bold;'>{l_natrijum}</p>
                <p style='margin: 5px 0px 0px 0px; color: {dnevna_n_boja}; font-size: 26px; font-weight: 900;'>{uk_n:.2f} mg</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        if st.button(t_dugme_obrisi):
            st.session_state['dnevnik_obroka'] = []
            st.rerun()
else:
    st.error("Baza podataka 'KPH-AI-GLOBAL.xlsx' nije pronađena ili je oštećena.")

# --- FUTER SA INFORMACIJAMA I BROJAČEM POSETA ---
st.write("---")
st.markdown("""
<div style='text-align: center; line-height: 1.2;'>
    <p style='margin: 0px; color: #ffffff; font-size: 14px;'>Ukupno poseta aplikaciji: <span style='color: #2ECC71; font-weight: bold;'>3010</span></p>
    <p style='margin: 5px 0px 0px 0px; font-weight: bold; color: #ffffff;'>♣️♦️♥️♠️ MAGICOMP & AI Gemini</p>
    <p style='margin: 0px; color: #279FF5;'>magy@usa.com &nbsp;&nbsp;|&nbsp;&nbsp; Tel.+38163310850</p>
    <p style='margin: 0px;  color: #888888; font-size: 12px;'>Powered by PYTHON</p>
</div>
""", unsafe_allow_html=True)
