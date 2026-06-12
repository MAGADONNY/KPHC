import streamlit as st
import pandas as pd

# Podešavanje izgleda web stranice (ikonica karte u tabu pretraživača)
st.set_page_config(page_title="Dnevnik Ishrane", page_icon="🃏", layout="centered")

# Forsiranje crne teme preko konfiguracije
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; font-size: 38px;'>♠️♥️Dnevnik Ishrane♦️♣️<br><span style='font-size: 22px; font-weight: normal;'>sa zbirom dnevnog unosa</span> </h1>", unsafe_allow_html=True)

# Tekst napomene odmah ispod naslova
st.write("⚠️ *Vrednosti minerala u tabeli su izražene u miligramima (mg) na 100 grama očišćene, sirove namirnice (osim ako nije drugačije naznačeno).*")

# Inicijalizacija liste obroka u memoriji stranice (ako već ne postoji)
if 'dnevnik_obroka' not in st.session_state:
    st.session_state['dnevnik_obroka'] = []

# Učitavanje baze uz preskakanje prvog praznog reda (header=1)
@st.cache_data
def ucitaj_bazu():
    try:
        df = pd.read_excel("KPH-AI.xlsx", header=1)
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor', 'Natrijum']
        df = df.dropna(subset=['Namirnica'])
        return df
    except Exception as e:
        st.error(f"Greška pri čitavanju Excel tabele: {e}")
        return None

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
        if st.button("➕ Dodaj obrok u moj dnevnik"):
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
        
        st.info("### 📊 UKUPAN DNEVNI ZBIR SVIH UNETIH OBROKA:")
        kol1, kol2, kol3 = st.columns(3)
        with kol1:
            st.metric(label="Ukupno Kalijum", value=f"{sum_k:.2f} mg")
        with kol2:
            st.metric(label="Ukupno Fosfor", value=f"{sum_f:.2f} mg")
        with kol3:
            st.metric(label="Ukupno Natrijum", value=f"{sum_n:.2f} mg")
            
        if st.button("🗑️ Isprazni kompletan dnevnik"):
            st.session_state['dnevnik_obroka'] = []
            st.rerun()
    else:
        st.write("Dnevnik je prazan. Izaberite namirnicu i dodajte obrok.")

# --- POTPIS AUTORA NA SAMOM DNU STRANICE ---
st.write("")
st.write("")
st.markdown("<p style='font-size: 18px; text-align: center; color: #808495;'>Autor: ♦️♣️♠️♥️ MAGICOMP & AI Gemini<br>magy@usa.com &nbsp;&nbsp; Tel.+38163310850</p>", unsafe_allow_html=True)
