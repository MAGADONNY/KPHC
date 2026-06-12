import streamlit as st
import pandas as pd

# Podešavanje naslova i izgleda web stranice
st.set_page_config(page_title="Dnevnik Ishrane", layout="centered")
st.title("🍏 Dnevnik Ishrane - Kalijum i Fosfor")

# Učitavanje baze iz vašeg Excel fajla koji je u istom folderu na GitHub-u
@st.cache_data
def ucitaj_bazu():
    try:
        df = pd.read_excel("KPH-AI.xlsx")
        
        # Automatski preimenujemo prve tri kolone bez obzira na ukupan broj kolona
        nove_kolone = list(df.columns)
        nove_kolone[0] = 'Namirnica'
        nove_kolone[1] = 'Kalijum'
        nove_kolone[2] = 'Fosfor'
        df.columns = nove_kolone
        
        return df
    except Exception as e:
        st.error(f"Greška pri učitavanju Excel tabele: {e}")
        return None

df = ucitaj_bazu()

if df is not None:
    st.subheader("🔍 Korak 1: Izaberite namirnicu")
    
    # Polje za pretragu uživo
    pretraga = st.text_input("Unesite naziv namirnice za pretragu (npr. hleb, piletina):")
    
    # Filtriranje baze na osnovu unetog teksta
    if pretraga:
        filtrirano = df[df['Namirnica'].astype(str).str.contains(pretraga, case=False, na=False)]
    else:
        filtrirano = df

    lista_namirnica = filtrirano['Namirnica'].dropna().tolist()
    
    if lista_namirnica:
        # Padajući meni sa pronađenim namirnicama
        izbor = st.selectbox("Izaberite tačnu namirnicu sa liste:", lista_namirnica)
        
        # Uzimanje vrednosti iz tabele za izabranu stavku (na 100g)
        red = df[df['Namirnica'] == izbor].iloc[0]
        
        # Pretvaranje u brojeve radi sigurnosti pri računanju
        k_vrednost = pd.to_numeric(red['Kalijum'], errors='coerce') if 'Kalijum' in red else 0
        f_vrednost = pd.to_numeric(red['Fosfor'], errors='coerce') if 'Fosfor' in red else 0
        
        st.info(f"Vrednosti na 100g -> Kalijum: {k_vrednost} mg | Fosfor: {f_vrednost} mg")
        
        st.write("---")
        st.subheader("⚖️ Korak 2: Unesite količinu")
        
        # Unos gramaže
        kolicina = st.number_input("Unesite količinu u gramima (g):", min_value=1.0, value=100.0, step=10.0)
        
        # Računanje vrednosti za unetu gramažu
        faktor = kolicina / 100.0
        ukupno_k = k_vrednost * faktor
        ukupno_f = f_vrednost * faktor
        
        # Prikaz konačnih rezultata korisniku u lepim kolonama
        st.success(f"### 📊 Rezultat za {kolicina}g namirnice **{izbor}**:")
        kol1, kol2 = st.columns(2)
        with kol1:
            st.metric(label="Ukupno Kalijum (mg)", value=f"{ukupno_k:.2f}")
        with kol2:
            st.metric(label="Ukupno Fosfor (mg)", value=f"{ukupno_f:.2f}")
    else:
        st.warning("Nijedna namirnica ne odgovara pretrazi. Pokušajte ponovo.")
