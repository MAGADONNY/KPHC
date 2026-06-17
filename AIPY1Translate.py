import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import io

st.title("🤖 Globalni prevodilac baze (SR ➡️ EN ➡️ ES ➡️ DE)")

@st.cache_data
def ucitaj_bazu():
    try:
        return pd.read_excel("KPH-AI.xlsx")
    except:
        return None

df = ucitaj_bazu()

if df is not None:
    st.write(f"📊 Učitano je **{len(df)}** namirnica.")
    
    if st.button("🚀 POKRENI AUTOMATSKI PREVOD NA ŠPANSKI I NEMAČKI"):
        progres_bar = st.progress(0)
        status_tekst = st.empty()
        
        prevodi_es = []
        prevodi_de = []
        ukupno = len(df)
        
        for i, n in enumerate(df['Namirnica'].tolist()):
            status_tekst.text(f"Prevođenje na ES i DE: {n}")
            
            # Sređivanje pre slanja Google-u
            t = str(n).lower()
            if "curetina" in t: t = t.replace("curetina", "ćuretina")
            if "skembici" in t: t = t.replace("skembici", "škembići")
            if "juneci" in t: t = t.replace("juneci", "juneći")
            if "karabatak" in t: t = t.replace("karabatak", "thigh")
            if "batak" in t: t = t.replace("batak", "drumstick")
            pojam = t.capitalize()
            
            # Prevod na Španski (es)
            try:
                p_es = GoogleTranslator(source='sr', target='es').translate(pojam)
                prevodi_es.append(p_es)
            except:
                prevodi_es.append(n)
                
            # Prevod na Nemački (de)
            try:
                p_de = GoogleTranslator(source='sr', target='de').translate(pojam)
                prevodi_de.append(p_de)
            except:
                prevodi_de.append(n)
                
            progres_bar.progress((i + 1) / ukupno)
            
        # Ubacivanje novih kolona u tabelu
        if 'Namirnica_ES' not in df.columns:
            df.insert(2, 'Namirnica_ES', prevodi_es)
        if 'Namirnica_DE' not in df.columns:
            df.insert(3, 'Namirnica_DE', prevodi_de)
            
        st.success("✅ Prevod na španski i nemački uspešno završen!")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        
        st.download_button(
            label="📥 PREUZMI GLOBALNU EXCEL BAZU",
            data=processed_data,
            file_name="KPH-AI-Global.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.error("❌ Program ne može da pronađe fajl 'KPH-AI.xlsx' na GitHub-u.")
