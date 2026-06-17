import streamlit as st
import pandas as pd
import os
from deep_translator import GoogleTranslator

# Podešavanje izgleda web stranice
st.set_page_config(page_title="Dnevnik Ishrane / Diet Diary", page_icon="🃏", layout="centered")

st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:4px;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#279FF5!important; border:none!important; width:100%!important; text-shadow:none!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#279FF5!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;}</style>", unsafe_allow_html=True)

# --- 🌐 LOGIKA ZA IZBOR JEZIKA ---
jezik = st.selectbox("🌐 Izaberite jezik / Select Language", ["Srpski", "English"])

# --- 📋 REČNIK FIKSNIH TEKSTOVA ---
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
    t_upozorenje = "No food items match your search. Please try another word."
    t_naslov_tabele = "📋 Your daily diet log and entered meals"
    t_zbir_okvir = "📊 TOTAL DAILY SUM OF ALL ENTERED MEALS:"
    t_ukupno_k = "Total Potassium: {:.2f} mg"
    t_ukupno_f = "Total Phosphorus: {:.2f} mg"
    t_ukupno_n = "Total Sodium: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Clear complete diary"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Food Item', 'Amount (g)', 'Potassium (mg)', 'Phosphorus (mg)', 'Sodium (mg)'
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
    t_upozorenje = "Nijedna namirnica ne odgovara pretrazi. Pokušajte ponovo."
    t_naslov_tabele = "📋 Vaš današnji dnevnik ishrane i uneti obroci"
    t_zbir_okvir = "📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:"
    t_ukupno_k = "Ukupno Kalijum: {:.2f} mg"
    t_ukupno_f = "Ukupno Fosfor: {:.2f} mg"
    t_ukupno_n = "Ukupno Natrijum: {:.2f} mg"
    t_dugme_obrisi = "🗑️ Isprazni kompletan dnevnik"
    col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum = 'Namirnica', 'Količina (g)', 'Kalijum (mg)', 'Fosfor (mg)', 'Natrijum (mg)'

# Prikaz zaglavlja
st.markdown(f"<h1 style='text-align: center; font-size: 38px;'>{t_naslov}</h1>", unsafe_allow_html=True)
st.write(t_napomena1)
st.write(t_napomena2)

if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    df = pd.read_excel("KPH-AI.xlsx", header=1)
    df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum']
    df = df.dropna(subset=['Namirnica'])
    return df

df = ucitaj_bazu()

if df is not None:
    st.write("")
    st.subheader(t_korak1)
    pretraga = st.text_input(t_input1, key="polje_pretrage")
    pojam_za_filter = pretraga.strip()
    
    # Prevodimo reč za pretragu na srpski ako je izabran engleski
    if pojam_za_filter and jezik == "English":
        try:
            pojam_za_filter = GoogleTranslator(source='en', target='sr').translate(pojam_za_filter)
        except:
            pass

    if pojam_za_filter:
        filtrirano = df[df['Namirnica'].astype(str).str.contains(pojam_za_filter, case=False, na=False)]
    else:
        filtrirano = df

    # Priprema liste namirnica sa limitom radi brzine
    lista_namirnica_prikaz = {}
    if not filtrirano.empty:
        za_prikaz = filtrirano.head(25) # Limitirano na top 25 radi brzine
        for n in za_prikaz['Namirnica'].tolist():
            if jezik == "English":
                try:
                    prevod_na_en = GoogleTranslator(source='sr', target='en').translate(n)
                    lista_namirnica_prikaz[prevod_na_en] = n
                except:
                    lista_namirnica_prikaz[n] = n
            else:
                lista_namirnica_prikaz[n] = n

    if lista_namirnica_prikaz:
        izbor_prikaz = st.selectbox(t_korak2, list(lista_namirnica_prikaz.keys()))
        izbor_original = lista_namirnica_prikaz[izbor_prikaz]
        
        # POPRAVLJENO: Dodat indeks [0] na iloc
        red = df[df['Namirnica'] == izbor_original].iloc[0]
        
        def ocisti_broj(vrednost):
            broj = pd.to_numeric(vrednost, errors='coerce')
            return 0 if pd.isna(broj) else broj

        k_v = ocisti_broj(red['Kalijum'])
        f_v = ocisti_broj(red['Fosfor'])
        n_v = ocisti_broj(red['Natrijum'])
        
        if k_v > 200:
            k_boja = "#ff4b4b"
        elif k_v < 100:
            k_boja = "#00ffcc"
        else:
            k_boja = "#ffffff"
            
        st.markdown(
            f"""
            <div style='background-color: #1e2430; padding: 15px; border-radius: 5px; border-left: 5px solid {k_boja};'>
                {t_okvir.format(f"<span style='color: {k_boja}; font-weight: bold;'>{k_v}</span>", f_v, n_v)}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.write("---")
        st.subheader(t_korak3)
        kolicina = st.number_input(t_input2, min_value=1.0, value=100.0, step=10.0)
        
        faktor = kolicina / 100.0
        ukupno_k = k_v * faktor
        ukupno_f = f_v * faktor
        ukupno_n = n_v * faktor
        
        st.markdown("<div class='veliko-dugme'>", unsafe_allow_html=True)
        izvrseno = st.button(t_dugme_dodaj)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if izvrseno:
            st.session_state['dnevnik_obroka'].append({
                'Namirnica': izbor_prikaz, 
                'Količina (g)': round(kolicina, 2),
                'Kalijum (mg)': round(ukupno_k, 2),
                'Fosfor (mg)': round(ukupno_f, 2),
                'Natrijum (mg)': round(ukupno_n, 2)
            })
            st.toast(t_toast.format(izbor_prikaz, kolicina), icon="✅")

    else:
        st.warning(t_upozorenje)

    # --- PRIKAZ DNEVNOG ZBIRA ---
    st.write("---")
    st.subheader(t_naslov_tabele)

    if st.session_state['dnevnik_obroka']:
        prikaz_df = pd.DataFrame(st.session_state['dnevnik_obroka'])
        prikaz_df.columns = [col_namirnica, col_kolicina, col_kalijum, col_fosfor, col_natrijum]
        
        def oboji_tabelu(red_tabele):
            boje = [''] * len(red_tabele)
            val = red_tabele[col_kalijum]
            k_na_100g = (val / red_tabele[col_kolicina]) * 100
            if k_na_100g > 200:
                boje[prikaz_df.columns.get_loc(col_kalijum)] = 'color: #ff4b4b; font-weight: bold;'
            elif k_na_100g < 100:
                boje[prikaz_df.columns.get_loc(col_kalijum)] = 'color: #00ffcc; font-weight: bold;'
            return boje

        st.dataframe(
            prikaz_df.style.apply(oboji_tabelu, axis=1).format({
                col_kolicina: '{:.2f}',
                col_kalijum: '{:.2f}',
                col_fosfor: '{:.2f}',
                col_natrijum: '{:.2f}'
            }), 
            use_container_width=True
        )
        
        sum_k = prikaz_df[col_kalijum].sum()
        sum_f = prikaz_df[col_fosfor].sum()
        sum_n = prikaz_df[col_natrijum].sum()
        
        boja_kalijuma = "#ff4b4b" if sum_k > 1199 else "#279FF5"
        
        st.markdown(f"""
<div style='font-size: 20px; font-weight: bold; line-height: 1.6; width: 100%;'>
    <div style='border: 2px solid #ffffff; padding: 10px; border-radius: 5px; color: #279FF5; margin-bottom: 20px; width: 100%; box-sizing: border-box;'>
        {t_zbir_okvir}
    </div>
    <span style='color: {boja_kalijuma};'>{t_ukupno_k.format(sum_k)}</span><br>
    <span style='color: #279FF5;'>{t_ukupno_f.format(sum_f)}</span><br>
    <span style='color: #279FF5;'>{t_ukupno_n.format(sum_n)}</span>
</div>
""", unsafe_allow_html=True)
            
        if st.button(t_dugme_obrisi):
            st.session_state['dnevnik_obroka'] = []
            st.rerun()

