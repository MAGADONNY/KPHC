import streamlit as st
import pandas as pd

# Podešavanje izgleda web stranice (ikonica karte u tabu pretraživača)
st.set_page_config(page_title="Dnevnik Ishrane by Magicom", page_icon="🃏", layout="centered")

st.markdown("<style>.stApp{background-color:#0e1117;color:#ffffff;} div[data-baseweb='input'] {background-color:#1e2430!important; border-radius:4px;} div[data-baseweb='input'] input, div[data-baseweb='input'] input:focus {color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; background-color:#1e2430!important;} div.stButton > button {font-weight:900!important; font-family:sans-serif!important; color:#000000!important; background-color:#279FF5!important; border:none!important; width:100%!important; text-shadow:none!important;} div.stButton > button:focus, div.stButton > button:active {color:#000000!important; background-color:#279FF5!important; font-weight:900!important;} label, div[data-testid='stWidgetLabel'] p {color:#ffffff!important; font-weight:bold!important; font-size:16px!important;}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 38px;'>♠️♥️Dnevnik Ishrane♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>provera nivoa minerala u namirnicama sa zbirom dnevnog unosa</span> </h1>", unsafe_allow_html=True)

# Tekst napomene odmah ispod naslova
st.write("⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice (osim ako nije drugačije naznačeno).*")
st.write("ⓘ *Preporuceni dnevni unos: Kalijum max 1200-1500mg | Fosfor max 800-1000mg *")

# Inicijalizacija liste obroka u memoriji stranice (ako već ne postoji)
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Učitavanje baze uz preskakanje prvog praznog reda (header=1)

@st.cache_data(ttl=86400)
def ucitaj_bazu():
    df = pd.read_excel("KPH-AI.xlsx", header=1)
    df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum']
    df = df.dropna(subset=['Namirnica'])
    return df

df = ucitaj_bazu()

if df is not None:
    st.write("") # Prazan prostor radi estetike
    st.subheader("🔍 Korak 1: Izaberite namirnicu iz baze podataka")
    pretraga = st.text_input("Unesite naziv namirnice za pretragu:")
    
    if pretraga:
        filtrirano = df[df['Namirnica'].astype(str).str.contains(pretraga, case=False, na=False)]
    else:
        filtrirano = df

    lista_namirnica = filtrirano['Namirnica'].tolist()
    
    if lista_namirnica:
        izbor = st.selectbox("Klikni i izaberi namirnicu sa liste:", lista_namirnica)
        
        # Filtriranje reda za izabranu namirnicu
        red = df[df['Namirnica'] == izbor].iloc[0]
        
        def ocisti_broj(vrednost):
            broj = pd.to_numeric(vrednost, errors='coerce')
            return 0 if pd.isna(broj) else broj

        k_v = ocisti_broj(red['Kalijum'])
        f_v = ocisti_broj(red['Fosfor'])
        n_v = ocisti_broj(red['Natrijum'])
        
        # LOGIKA ZA BOJU KALIJUMA (Na 100g)
        if k_v > 200:
            k_boja = "#ff4b4b" # Crvena
        elif k_v < 100:
            k_boja = "#00ffcc" # Jarko zelena
        else:
            k_boja = "#ffffff" # Bela
            
        # Prikaz sa obojenim Kalijumom u lepom okviru
        st.markdown(
            f"""
            <div style='background-color: #1e2430; padding: 15px; border-radius: 5px; border-left: 5px solid {k_boja};'>
                Vrednosti na 100g -> 
                <span style='color: {k_boja}; font-weight: bold; font-size: 17px;'>Kalijum: {k_v} mg</span> | 
                Fosfor: {f_v} mg | 
                Natrijum: {n_v} mg
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.write("---")
        st.subheader("⚖️ Korak 2: Upisite kolicinu konzumirane namirnice")
        
        kolicina = st.number_input("Unesite ovde tačnu težinu u gramima (g):", min_value=1.0, value=100.0, step=10.0)
        
        faktor = kolicina / 100.0
        ukupno_k = k_v * faktor
        ukupno_f = f_v * faktor
        ukupno_n = n_v * faktor
        
        # Dugme za dodavanje namirnice u dnevni zbir
        st.markdown("<div class='veliko-dugme'>", unsafe_allow_html=True)
        izvrseno = st.button("➕ Dodaj obrok u moj dnevnik")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if izvrseno:
            st.session_state['dnevnik_obroka'].append({
                'Namirnica': izbor,
                'Količina (g)': round(kolicina, 2),
                'Kalijum (mg)': round(ukupno_k, 2),
                'Fosfor (mg)': round(ukupno_f, 2),
                'Natrijum (mg)': round(ukupno_n, 2)
            })
            st.toast(f"Dodato u dnevnik: {izbor} ({kolicina}g)", icon="✅")

    else:
        st.warning("Nijedna namirnica ne odgovara pretrazi. Pokušajte ponovo.")

    # --- PRIKAZ DNEVNOG ZBIRA ---
    st.write("---")
    st.subheader("📋 Vaš današnji dnevnik ishrane i uneti obroci")

    if st.session_state['dnevnik_obroka']:
        prikaz_df = pd.DataFrame(st.session_state['dnevnik_obroka'])
        
        # Funkcija koja boji samo cifru Kalijuma u tabeli
        def oboji_tabelu(red_tabele):
            boje = [''] * len(red_tabele)
            val = red_tabele['Kalijum (mg)']
            k_na_100g = (val / red_tabele['Količina (g)']) * 100
            
            if k_na_100g > 200:
                boje[prikaz_df.columns.get_loc('Kalijum (mg)')] = 'color: #ff4b4b; font-weight: bold;'
            elif k_na_100g < 100:
                boje[prikaz_df.columns.get_loc('Kalijum (mg)')] = 'color: #00ffcc; font-weight: bold;'
            return boje

        # Formatiramo prikaz tabele na dve decimale (.format("{:.2f}"))
        st.dataframe(
            prikaz_df.style.apply(oboji_tabelu, axis=1).format({
                'Količina (g)': '{:.2f}',
                'Kalijum (mg)': '{:.2f}',
                'Fosfor (mg)': '{:.2f}',
                'Natrijum (mg)': '{:.2f}'
            }), 
            use_container_width=True
        )
        
        sum_k = prikaz_df['Kalijum (mg)'].sum()
        sum_f = prikaz_df['Fosfor (mg)'].sum()
        sum_n = prikaz_df['Natrijum (mg)'].sum()
        
        boja_kalijuma = "#ff4b4b" if sum_k > 1199 else "#279FF5"
        
        st.markdown(f"""
<div style='font-size: 20px; font-weight: bold; line-height: 1.6; width: 100%;'>
    <div style='border: 2px solid #ffffff; padding: 10px; border-radius: 5px; color: #279FF5; margin-bottom: 20px; width: 100%; box-sizing: border-box;'>
        📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:
    </div>
    <span style='color: {boja_kalijuma};'>Ukupno Kalijum: {sum_k:.2f} mg</span><br>
    <span style='color: #279FF5;'>Ukupno Fosfor: {sum_f:.2f} mg</span><br>
    <span style='color: #279FF5;'>Ukupno Natrijum: {sum_n:.2f} mg</span>
</div>
""", unsafe_allow_html=True)
            
        if st.button("🗑️ Isprazni kompletan dnevnik"):
            st.session_state['dnevnik_obroka'] = []
            st.rerun()
# --- LOGIKA ZA INTERNI BROJAČ POSETA ---
import os

ime_fajla = "brojac.txt"
pocetni_broj = 3002

if 'poseta_uracunata' not in st.session_state:
    if not os.path.exists(ime_fajla):
        with open(ime_fajla, "w") as f:
            f.write(str(pocetni_broj))
        trenutni_broj = pocetni_broj
    else:
        with open(ime_fajla, "r") as f:
            try:
                trenutni_broj = int(f.read().strip()) + 1
            except:
                trenutni_broj = pocetni_broj
        with open(ime_fajla, "w") as f:
            f.write(str(trenutni_broj))
    st.session_state['poseta_uracunata'] = trenutni_broj
else:
    if os.path.exists(ime_fajla):
        with open(ime_fajla, "r") as f:
            try:
                trenutni_broj = int(f.read().strip())
            except:
                trenutni_broj = pocetni_broj
    else:
        trenutni_broj = pocetni_broj

st.write("")
st.write("")

# Prikaz brojača kao čist HTML tekst
st.markdown(f"""
<div style='text-align: center; margin-bottom: 15px;'>
    <p style='color: #808495; font-size: 16px; margin-bottom: 5px;'>
         Ukupno poseta aplikaciji: <span style='color: #279FF5; font-weight: bold;'>{trenutni_broj}</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Potpis autora na samom dnu
st.markdown("""
<p style='font-size: 18px; text-align: center; color: #808495;'>
Autor: ♦️♣️♠️♥️ MAGICOMP & AI Gemini<br>
magy@usa.com &nbsp;&nbsp; Tel.+38163310850<br>
Powered by PYTHON
</p>
""", unsafe_allow_html=True)

            
