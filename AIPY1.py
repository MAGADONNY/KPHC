import streamlit as st
import pandas as pd

# Podešavanje izgleda web stranice
st.set_page_config(page_title="Dnevnik Ishrane", layout="centered")
st.title("🍏 Dnevnik Ishrane - Sa Dnevnim Zbirom")

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
    st.subheader("🔍 Korak 1: Izaberite namirnicu")
    pretraga = st.text_input("Unesite naziv namirnice za pretragu (npr. svinjetina, govedina):")
    
    if pretraga:
        filtrirano = df[df['Namirnica'].astype(str).str.contains(pretraga, case=False, na=False)]
    else:
        filtrirano = df

    lista_namirnica = filtrirano['Namirnica'].tolist()
    
    if lista_namirnica:
        izbor = st.selectbox("Izaberite tačnu namirnicu sa liste:", lista_namirnica)
        
        # Filtriranje reda za izabranu namirnicu
        red = df[df['Namirnica'] == izbor].iloc[0]
        
        def ocisti_broj(vrednost):
            broj = pd.to_numeric(vrednost, errors='coerce')
            return 0 if pd.isna(broj) else broj

        k_v = ocisti_broj(red['Kalijum'])
        f_v = ocisti_broj(red['Fosfor'])
        n_v = ocisti_broj(red['Natrijum'])
        
        st.info(f"Vrednosti na 100g -> Kalijum: {k_v} mg | Fosfor: {f_v} mg | Natrijum: {n_v} mg")
        
        st.write("---")
        st.subheader("⚖️ Korak 2: Unesite količinu i dodajte u dnevnik")
        
        kolicina = st.number_input("Unesite količinu u gramima (g):", min_value=1.0, value=100.0, step=10.0)
        
        faktor = kolicina / 100.0
        ukupno_k = k_v * faktor
        ukupno_f = f_v * faktor
        ukupno_n = n_v * faktor
        
        # Dugme za dodavanje namirnice u dnevni zbir
        if st.button("➕ Dodaj u dnevni zbir"):
            st.session_state['dnevnik_obroka'].append({
                'Namirnica': izbor,
                'Količina (g)': kolicina,
                'Kalijum (mg)': ukupno_k,
                'Fosfor (mg)': ukupno_f,
                'Natrijum (mg)': ukupno_n
            })
            st.toast(f"Dodato: {izbor} ({kolicina}g)", icon="✅")

    else:
        st.warning("Nijedna namirnica ne odgovara pretrazi. Pokušajte ponovo.")

    # --- PRIKAZ DNEVNOG ZBIRA ---
    st.write("---")
    st.subheader("📋 Vaš današnji dnevnik ishrane")

    if st.session_state['dnevnik_obroka']:
        prikaz_df = pd.DataFrame(st.session_state['dnevnik_obroka'])
        
        st.dataframe(prikaz_df, use_container_width=True)
        
        sum_k = prikaz_df['Kalijum (mg)'].sum()
        sum_f = prikaz_df['Fosfor (mg)'].sum()
        sum_n = prikaz_df['Natrijum (mg)'].sum()
        
        st.info("### 📊 UKUPAN DNEVNI ZBIR:")
        kol1, kol2, kol3 = st.columns(3)
        with kol1:
            st.metric(label="Ukupno Kalijum", value=f"{sum_k:.2f} mg")
        with kol2:
            st.metric(label="Ukupno Fosfor", value=f"{sum_f:.2f} mg")
        with kol3:
            st.metric(label="Ukupno Natrijum", value=f"{sum_n:.2f} mg")
            
        if st.button("🗑️ Isprazni dnevnik"):
            st.session_state['dnevnik_obroka'] = []
            st.rerun()
    else:
        st.write("Još uvek niste dodali nijednu namirnicu za danas.")
