import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import io

st.title("🤖 Fino podešavanje i poravnanje engleskih naziva")

@st.cache_data
def ucitaj_bazu():
    try:
        return pd.read_excel("KPH-AI.xlsx")
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    st.write(f"📊 Baza je uspešno učitana. Ukupno ima **{len(df)}** stavki.")
    
    if st.button("🚀 POKRENI FINO PORAVNANJE ENGLESKOG JEZIKA"):
        progres_bar = st.progress(0)
        status_tekst = st.empty()
        
        novi_prevodi_en = []
        ukupno = len(df)
        
        for i, n in enumerate(df[df.columns[0]].tolist()):
            tekst = str(n).strip()
            status_tekst.text(f"Poravnanje ({i+1}/{ukupno}): {tekst}")
            
            if tekst and tekst != "nan":
                t = tekst.lower()
                if "curetina" in t: t = t.replace("curetina", "ćuretina")
                if "skembici" in t: t = t.replace("skembici", "škembići")
                if "juneci" in t: t = t.replace("juneci", "juneći")
                if "karabatak" in t: t = t.replace("karabatak", "thigh")
                if "batak" in t: t = t.replace("batak", "drumstick")
                pojam = t.capitalize()
                
                try:
                    p_en = GoogleTranslator(source='sr', target='en').translate(pojam)
                    p_en = p_en.replace("Drumstick, drumstick", "Drumstick").replace("Thigh, thigh", "Thigh")
                    novi_prevodi_en.append(p_en)
                except:
                    novi_prevodi_en.append(tekst)
            else:
                novi_prevodi_en.append("")
                
            progres_bar.progress((i + 1) / ukupno)
            
        # Menjamo staru kolonu B sa novim, tačnim i poravnatim prevodom
        df[df.columns[1]] = novi_prevodi_en
        st.success("✅ Engleski jezik je uspešno poravnat i spakovan!")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 PREUZMI KONAČNU GLOBALNU BAZU",
            data=processed_data,
            file_name="KPH-AI-Globalna.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
