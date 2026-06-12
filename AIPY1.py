import streamlit as st
import pandas as pd

# Podešavanje naslova na web stranici
st.set_page_config(page_title="Dnevnik Ishrane", layout="centered")
st.title("🍏 Dnevnik Ishrane - Kalijum i Fosfor")

# Učitavanje baze iz istog foldera na GitHub-u
@st.cache_data
def ucitaj_bazu():
    try:
        # Čitanje Excel tabele
        df = pd.read_excel("KPH-AI.xlsx")
        # Postavljanje naziva kolona (promenite ako se u vašem Excelu zovu drugačije)
        df.columns = ['Namirnica', 'Kalijum', 'Fosfor']
        return df
    except Exception as e:
        st.error(f"Greška pri učitavanju baze podaci: {e}")
        return None

df = ucitaj_bazu()

if df is not None:
    st.subheader("🔍 Pretraga i unos")
    
    # Polje za unos teksta za pretragu
    pretraga = st.text_input("Unesite naziv namirnice (npr. hleb, piletina):")
    
    # Filtriranje baze
    if pretraga:
        filtrirano = df[df['Namirnica'].str.contains(pretraga, case=False, na=False)]
    else:
        filtrirano = df

    lista_namirnica = filtrirano['Namirnica'].tolist()
    
    if lista_namirnica:
        # Padajući meni sa pronađenim namirnicama
        izbor = st.selectbox("Izaberite tačnu namirnicu:", lista_namirnica)
        
        # Uzimanje vrednosti za izabranu stavku
        red = df[df['Namirnica'] == izbor].iloc[0]
        st.text(f"Vrednosti na 100g -> Kalijum: {red['Kalijum']}mg | Fosfor: {red['Fosfor']}mg")
        
        st.write("---")
        
        # Unos gramaže
        kolicina = st.number_input("Unesite količinu u gramima (g):", min_value=1.0, value=100.0, step=10.0)
        
        # Računanje vrednosti za unetu gramažu
        faktor = kolicina / 100.0
        ukupno_k = red['Kalijum'] * faktor
        ukupno_f = red['Fosfor'] * faktor
        
        # Prikaz rezultata korisniku
        st.success(f"### 📊 Rezultat za {kolicina}g:")
        kol1, kol2 = st.columns(2)
        with kol1:
            st.metric(label="Ukupno Kalijum", value=f"{ukupno_k:.2f} mg")
        with kol2:
            st.metric(label="Ukupno Fosfor", value=f"{ukupno_f:.2f} mg")
    else:
        st.warning("Nema pronađenih namirnica sa tim nazivom.")
